///////////////////// Affichage du Cube ///////////////////////////
#include "affichage_cube.h"     // Bbiliothèque pour avoir un affichage sur le moniteur série du cube
#include "movements.h"          // Bibliothèque des mouvements réalisés par le cube
 
///////////////////// Algorithme mouvement ///////////////////////////
#include "fix_cross.h"          // Bibliothèque pour les mouvements de la croix centrale
#include "fix_corners.h"        // Bibliothèque pour les mouvements des coins
#include "edges.h"              // Bibliothèque pour les mouvements de la deuxième couronne
#include "white_cross.h"        // Bibliothèque pour les mouvements de la face arrière 
#include "fix_last_corners.h"   // Bibliothèque pour les mouvements des dernier angles 
#include "rotation.h"           // Bibliottèque pour définir les rotations spatiales du cube

//////////////////////////////// Algorithme décision ///////////////////////
# include "solve_cross.h"       // Bibliothèque de décision pour réaliser la première croix non orientée
# include "solve_total_cross.h" // Bibliothèque de décision pour réaliser la première croix orientée
# include "solve_corners.h"     // Bibliothèque de décision pour réaliser la première face
# include "solve_second_layer.h"// Bibliothèque de décision pour réaliser la deuxième couronne
# include "solve_other_cross.h" // Bibliothèque de décision pour réaliser la croix opposée à la première face
# include "solve_rear_face.h"   // Bibliothèque de décision pour réaliser la face opposée à la première face
# include "solve_last_angle.h"  // Bibliothèque de décision pour orienter les coins de la face opposée
# include "solve_last_cube.h"   // Bibliothèque de décision pour terminer le cube
# include "solve_verification.h"// Bibliothèque qui vérifie si le cube est bien résolu

//////////////////////////////// Declaration des variables ///////////////////////
char r_face_j[9];
char r_face_b[9];
char r_face_bl[9];
char r_face_v[9];
char r_face_r[9];
char r_face_o[9];

int solve_stage = 1;
bool cube_solved = true;
int n;

/////////////////////////////// Implémentation variable lecture python ////////////////////////////////////////////////////
char datafromUser;    // Variable pour la lecture du moniteur série
String cube = "";     // Initialisation d'un compteur  
// "w r b o g y"
int count = 0;
String p;             // variable tampon
int q;                // variable tampon

// Définition des variables de réception de python pour chaque couleur
String yellow="";
String white="";;
String blue="";;
String red="";;
String green="";;
String orange="";;

// Définition des six faces du cube
char face_j[9]={'y','y','y','y','y','y','y','y','y'};
char face_bl[9]={'w','w','w','w','w','w','w','w','w'};
char face_b[9]={'b','b','b','b','b','b','b','b','b'};
char face_r[9]={'r','r','r','r','r','r','r','r','r'};
char face_v[9]={'g','g','g','g','g','g','g','g','g'};
char face_o[9]={'o','o','o','o','o','o','o','o','o'};


void color_choice(String color, char color_side[9]) {   // Procédure de conversion entre python et Arduino

  for(int j=0;j<9;j++) {                                // Pour la couleur donnée, on étudie chaque cube 
        p=color[j];                                     // On convertit la couleur du cube en nombre (cela implique que les couleurs sont définies par des nombres)
        q=p.toInt();
        if (q == 1){color_side[j]='b';}                 // Si la variable vaut 1, la couleur est bleue
        else if (q == 2){color_side[j] = 'y';}          // Si la variable vaut 2, la couleur est jaune
        else if (q == 3){color_side[j] = 'o';}          // Si la variable vaut 3, la couleur est orange
        else if (q == 4){color_side[j] = 'g';}          // Si la variable vaut 4, la couleur est vert
        else if (q == 5){color_side[j] = 'r';}          // Si la variable vaut 5, la couleur est rouge
        else if (q == 6){color_side[j] = 'w';}          // Si la variable vaut 6, la couleur est blanche
             else {Serial.println("ERREUR");}}          // Sinon, il y a une erreur dans le cube
}

//////////////////////////////// Séquence de résolution ///////////////////////////////////////////////////
void cube_decide(){
        switch(solve_stage){
                case 1: // 1ère croix
                        cube_decide_cross(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_1(solve_stage);
                        n = get_global_1();
                        if (n==2) {solve_stage=2;}
                        break;
                        
                case 2: // orientation de la croix
                        cube_decide_whole_cross(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_2(solve_stage);
                        n = get_global_2();
                        if (n==3) {solve_stage=3;}
                        break;
                        
                case 3: // Corners (1ère face)
                        cube_decide_corners(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_3(solve_stage);
                        n = get_global_3();
                        if (n==4) {solve_stage=4;}
                        break;
                        
                case 4: // Deuxième ligne
                        cube_decide_add_edges(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_4(solve_stage);
                        n = get_global_4();
                        if (n==5) {solve_stage=5;}
                        break;
                        
                case 5: // Croix blanche
                        cube_decide_white_cross(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_5(solve_stage);
                        n = get_global_5();
                        if (n==6) {solve_stage=6;}
                        break;
                        
                case 6: // Face blanche
                        cube_decide_white_top(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_6(solve_stage);
                        n = get_global_6();
                        if (n==7) {solve_stage=7;}
                        break;
                        
                case 7: // Orientation des derniers angles
                        cube_decide_oll(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_7(solve_stage);
                        n = get_global_7();
                        if (n==8) {solve_stage=8;}
                        break;
                        
                case 8: // Permutation de la dernière couche
                        cube_decide_pll(solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v,r_face_r, face_r, r_face_o, face_o);
                        set_global_8(solve_stage);
                        n = get_global_8();
                        if (n==9) {solve_stage=9;}
                        break;
                        
                case 9:
                        cube_decide_solved(cube_solved, solve_stage, r_face_j, face_j, r_face_b, face_b,r_face_bl, face_bl, r_face_v, face_v, r_face_r, face_r, r_face_o, face_o);
                        set_global_9(solve_stage);
                        n = get_global_9();
                        if (n==10) {solve_stage=10;}
                        break;
        }
}

// Résolution du cube
void solve_cube(){
        Serial.println("Solving Cube: ");
        print_whole_cube(face_j, face_bl, face_b, face_r, face_v, face_o);
        solve_stage = 1;
        while(solve_stage != 10){cube_decide();}
}

void setup(){Serial.begin(9600);} // Définition du moniteur série   

void loop(){
  ///////////////////////////////Lecture python//////////////////////////////////////////
  while(true) {
     while(Serial.available() > 0){                         // S'il y a quelque chose qui est écrit dans le moniteur série        
      datafromUser=Serial.read();                           // On lit le moniteur série
      if (count<9) {yellow.concat(datafromUser);}           // On commence par la couleur jaune
      else if (count<18) {blue.concat(datafromUser);}       // Puis la couleur bleue
      else if (count<27) {white.concat(datafromUser);}      // Puis la couleur blanche
      else if (count<36) {red.concat(datafromUser);}        // Puis la couleur rouge
      else if (count<45) {green.concat(datafromUser);}      // Puis la couleur verte
      else if (count<54) {orange.concat(datafromUser);}     // Et enfin la couleur orange
    count+=1;                                               // Incrémente le compteur
  }

   // Si l'entièreté du vecteur python a été transféré
  if (count>=54 && count<= 55) {
     Serial.println("Transfert finish ...");
      delay(500);
      
      color_choice(yellow, face_j);                         // Appelle de la procédure pour la couleur jaune
      color_choice(blue, face_b);                           // Appelle de la procédure pour la couleur bleue       
      color_choice(white, face_bl);                         // Appelle de la procédure pour la couleur blanche  
      color_choice(red, face_r);                            // Appelle de la procédure pour la couleur rouge  
      color_choice(green, face_v);                          // Appelle de la procédure pour la couleur vert 
      color_choice(orange, face_o);                         // Appelle de la procédure pour la couleur orange
      delay(2000);
      count=100;
      }

      if(count==100) {break;}
  }

  ///////////////////////////////Résolution cube//////////////////////////////////////////
  solve_cube();
  Serial.println("Done!");
  while(true){}
  };
