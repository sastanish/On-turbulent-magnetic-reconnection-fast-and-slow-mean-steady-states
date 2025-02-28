#include <bout/derivs.hxx>
#include <bout/invert/laplacexz.hxx>
#include <bout/physicsmodel.hxx>
#include <bout/smoothing.hxx>

class trm : public PhysicsModel {
private:

  Field3D vort, j_par;
  Field3D phi, psi;
  Field3D K, W;

  // Model parameters
  BoutReal Rm, Re;
  BoutReal D_Rm, D_Re;
  BoutReal C_b, C_g, C_w, tau;
  BoutReal chi, K_min;

  // Poisson brackets: b0 x Grad(f) dot Grad(g) / B = [f, g]
  // Method to use: BRACKET_ARAKAWA, BRACKET_STD or BRACKET_SIMPLE
  BRACKET_METHOD bm; // Bracket method for advection terms

  std::unique_ptr<LaplaceXZ> psiSolver; // Laplacian solver for vort -> psi
                                        //
protected:
  int init(bool UNUSED(restart)) {

    auto& globalOption = Options::root();

    auto& options = Options::root()["trm"];
    Re = options["Re"].withDefault(1e4);
    Rm = options["Rm"].withDefault(1e4);

    C_b = options["C_b"].withDefault(0.3);
    C_g = options["C_g"].withDefault(0.3);
    C_w = options["C_w"].withDefault(1.3);
    tau = options["tau"].withDefault(1.0);
    chi = options["chi"].withDefault(1e-6);
    K_min = options["K_min"].withDefault(1e-8);

    D_Rm = 1/Rm;
    D_Re = 1/Re;

    SOLVE_FOR(phi,vort,K,W);
    SAVE_REPEAT(psi);
    SAVE_REPEAT(j_par);

    psiSolver = LaplaceXZ::create(mesh, &Options::root()["psiSolver"]);
    psiSolver->setCoefs(Field2D(1.0), Field2D(0.0));

    psi = 0.; // Starting phi
    j_par = -1*Delp2(phi); // Starting j

    // Choose method to use for Poisson bracket advection terms
    switch (options["bracket"].withDefault(0)) {
    case 0: {
      bm = BRACKET_STD;
      output << "\tBrackets: default differencing\n";
      break;
    }
    case 1: {
      bm = BRACKET_SIMPLE;
      output << "\tBrackets: simplified operator\n";
      break;
    }
    case 2: {
      bm = BRACKET_ARAKAWA;
      output << "\tBrackets: Arakawa scheme\n";
      break;
    }
    case 3: {
      bm = BRACKET_CTU;
      output << "\tBrackets: Corner Transport Upwind method\n";
      break;
    }
    default:
      output << "ERROR: Invalid choice of bracket method. Must be 0 - 3\n";
      return 1;
    }

    return 0;
  }

  int rhs(BoutReal t) override {

    psi = psiSolver->solve(-1*vort, psi);
    mesh->communicate(psi,vort,K,W,phi);

    j_par = -1*Delp2(phi);
    mesh->communicate(j_par);

    BOUT_FOR(i, K.getMesh()->getRegion3D("RGN_ALL")) {
      if (K[i] < K_min) K[i] = K_min;
    };

    ddt(vort) = bracket(vort, psi, bm) + bracket(phi,j_par,bm) + D_Re * Delp2(vort);
    ddt(phi) =  bracket(phi, psi, bm) - (D_Rm + C_b*tau*K) * j_par + C_g*tau*W*vort;
    ddt(W) = bracket(W,psi,bm) + bracket(phi,K,bm) + C_b*tau*K*j_par*vort - C_g*tau*W*pow(vort,2) - C_w*W/tau - chi*Delp2(Delp2(W));
    ddt(K) = bracket(K,psi,bm) + bracket(phi,W,bm) + C_b*tau*K*pow(j_par,2) - C_g*tau*W*j_par*vort - K/tau - chi*Delp2(Delp2(K));

    return 0;
  }

};

BOUTMAIN(trm);
