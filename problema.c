
/**
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
//#include <iostream>
//#include <uuid/uuid.h>
#include "rebound.h"
#include "tools.h"
#include "output.h"



// void heartbeat(struct reb_simulation* const r);

int main(int argc, char* argv[]){
    struct reb_simulation* r = reb_create_simulation();
    //struct reb_simulation* r2 = reb_create_simulation();
    r->G         = 1;
    //r2->G        = 1;
    const double e_test =atof(argv[1]);
    const double a_test = atof(argv[2]);
    const double ang_test = atof(argv[3]);
    const double ang_test_rad=ang_test*M_PI/180;
    const int bins = atoi(argv[4]);

    const double m = 2.5e-7/((double)bins);
    //const double tau0 = pow(N, 0.5)*pow(m*bins, 2)/a_test;
    //    printf("%e\n", tau0);
    // Initial conditions
    struct reb_particle star = {0};
    star.m = 1;
    reb_add(r, star);
    //struct reb_particle star2 = {0};
    /* star2.m = 1; */
    /* reb_add(r2, star2); */
    for (int j=0; j<bins; j++){
        struct reb_particle pt, pt2;
        double M = (j)*((2.*M_PI)/(double)bins);
        //double M = M_PI;
	//double M = reb_random_uniform(0, 2.*M_PI);
        double f = reb_tools_M_to_f(e_test, M);
        pt = reb_tools_orbit_to_particle(r->G, r->particles[0], 1.0e3*m, 1., e_test, 0.1*M_PI/180., 0, 0, f);
        //pt = reb_tools_orbit2d_to_particle(r->G, r->particles[0], 1.0e3*m, 1.0, e_test, 0, f);
        reb_add(r, pt);

    }
    double* farr=malloc(bins*sizeof(double));
    for (int j=0; j<bins; j++){
        struct reb_particle pt, pt2;
        //printf("%f\n", j*((2.*M_PI)/(double)bins));
        double M = (j)*((2.*M_PI)/(double)bins);
        //double M = M_PI;
        //double M = reb_random_uniform(0, 2.*M_PI);
        double f = reb_tools_M_to_f(e_test, M);
        farr[j]=f;
        pt = reb_tools_orbit2d_to_particle(r->G, r->particles[0], m, a_test, e_test, ang_test_rad, f);
        reb_add(r, pt);
      
    }
    double ex=e_test*cos(ang_test*M_PI/180);
    double ey=e_test*sin(ang_test*M_PI/180);
    //reb_simulationarchive_snapshot(r, "test.bin");
    //    printf("%s\n",ii);

    // reb_move_to_com(r);
   double* tauz2 = malloc(bins*sizeof(double));
   double* tauz3 = malloc(bins*sizeof(double));

    double c = 0;
    double c1 = 0;
    double c2 = 0;
    double c3 = 0;
    double* c4 = malloc(bins*sizeof(double));
    double tt = 0;
    double yy = 0;
//    double* forceTot= malloc(3*sizeof(double));
    double forcexTot=0;
    double forceyTot=0;
    double forcezTot=0;

    double taux=0;
    double tauy=0;
    double tauz=0;
    double tauzTot=0;
    double edotx=0;
    double edoty=0;
    double jz=0;
    double ieDot2=0;
    double ieDot3=0;
    double pre=1.0;
    double tmp=0;

    for (int i=1; i<bins+1; i++){
        double x=r->particles[i].x;
        double y=r->particles[i].y;
        double z=r->particles[i].z;
        for (int j=1; j<bins+1; j++){
           if (i==1){
               tauz2[j]=0;
               c4[j]=0;
           }
           if (j==1){
               tauz3[i-1]=0;
           }
            double xTest=r->particles[bins+j].x;
            double yTest=r->particles[bins+j].y;
            double zTest=r->particles[bins+j].z;
            double vx=r->particles[bins+j].vx;
            double vy=r->particles[bins+j].vy;
            double vz=r->particles[bins+j].vz;
            //Planar orbit
            vz=0;
            double phi = farr[j-1];
            // printf("%f %f\n", phi, vz);


            double d=pow(pow(x-xTest, 2.)+pow(y-yTest,2.)+pow(z-zTest,2.),0.5);
            double forcex = -1.0e3*pow(m,2.0)/pow(d,3.0)*(xTest-x);
            double forcey = -1.0e3*pow(m,2.0)/pow(d,3.0)*(yTest-y);
            double forcez = -1.0e3*pow(m,2.0)/pow(d,3.0)*(zTest-z);

            forcexTot+=forcex;
            forceyTot+=forcey;
            forcezTot+=forcez;

            taux= (yTest*forcez-zTest*forcey);
            tauy= -(xTest*forcez-zTest*forcex);
            tauz= (xTest*forcey-yTest*forcex);
            //     printf("%f %e %f %e %e %e\n", xTest,forcey,yTest, forcex, d, tauz);
            //Integration by simpson's 3/8 rule -- note that first coefficient is modified to account for segment between two endpoints
            /* if ((j==1)||(j==bins)){ */
            /*     pre=0.75; */
            /* }     */
            /* else if ((j-1)%3==0){ */
            /*     pre=0.75; */
            /* } */
            /* else{ */
            /*     pre=1.125; */
            /* } */
            yy=pre*tauz-c;
            tt=tauzTot+yy;
            c=(tt-tauzTot)-yy;
            tauzTot= tt;
            //Angular momentum of test orbit--Take this to be in the xy plane
            jz = xTest*vy-yTest*vx;
            double fr=forcex*cos(phi+ang_test_rad)+forcey*sin(phi+ang_test_rad);
            double vr=vx*cos(phi+ang_test_rad)+vy*sin(phi+ang_test_rad);

            //edotx += (forcey*jz)+(vy*tauz-vz*tauy);
            //edoty +=  -(forcex*jz)-(vx*tauz-vz*taux);
            yy= (forcey*jz)+(vy*tauz-vz*tauy)-c1;
            tt= edotx+yy;
            c1 = (tt-edotx)-yy;
            edotx = tt;

            yy= -(forcex*jz)-(vx*tauz-vz*taux)-c2;
            tt= edoty+yy;
            c2 = (tt-edoty)-yy;
            edoty = tt;

            tmp = pre*(-jz*fr/e_test*(cos(phi))+tauz*vr/e_test*(2/e_test+cos(phi)));
            yy=  tmp-c3;
            tt=  ieDot2+yy;
            c3= (tt-ieDot2)-yy;
            ieDot2= tt;
            // ieDot3+= -jz*fr/e_test*(cos(phi))+tauz*vr/e_test*(2/e_test+cos(phi));


//          Compensated summation for improved accuracy
//          double y = (xTest*forcey-yTest*forcex) - c;
//	    double t = tauz + y;
//	    c = (t - tauz) - y;

           yy= (tauz)-c4[j-1];
           tt= tauz2[j-1]+yy;
           c4[j]=(tt-tauz2[j-1])-yy;
           tauz2[j-1]=tt;
           if (j==bins/2){
               tauz3[i-1]=tauz3[i-1] +(xTest*forcey-yTest*forcex);
           }
       }

    }
    double ieDot=(ex*edoty-ey*edotx)/pow(e_test, 2.);

    char iname[80]="";
    strcat(iname, "i_");
    for (int i=1; i<4; i++){
        strcat(iname, "_");
        strcat(iname, argv[i]);
    }
    printf("%s\n",iname);
    FILE *ii=fopen(iname, "w");
    fprintf(ii, "%0.10e\n", ieDot2);
    fclose(ii);

    char fname[80]="";
    strcat(fname, "tau_");
    for (int i=1; i<4; i++){
        strcat(fname, "_");
        strcat(fname, argv[i]);
    }
    printf("%s\n",fname);
    FILE *f=fopen(fname, "w");
    fprintf(f, "%0.10e\n", tauzTot);
    fclose(f);

   char fname2[80]="";
   strcat(fname2, "tau_bin_");
   for (int i=1; i<4; i++){
       strcat(fname2, "_");
       strcat(fname2, argv[i]);
   }
   printf("%s\n",fname2);
   FILE *f2=fopen(fname2, "w");

   for (int j=1; j<bins+1; j++){
       double xTest=r->particles[bins+j].x;
       double yTest=r->particles[bins+j].y;
       fprintf(f2, "%lf %lf %e\n", xTest, yTest, tauz2[j-1]);
   }
   fclose(f2);

   // char fname3[80]="";
   // strcat(fname3, "tau_bin_b_");
   // for (int i=1; i<4; i++){
   //     strcat(fname3, "_");
   //     strcat(fname3, argv[i]);
   // }
   // printf("%s\n",fname3);
   // FILE *f3=fopen(fname3, "w");

   // for (int j=1; j<bins+1; j++){
   //     double xTest=r->particles[j].x;
   //     double yTest=r->particles[j].y;
   //     // double MTest=reb_tools_f_to_M(e_test, r->particles[j].f);
   //     fprintf(f3, "%lf %lf %e\n", xTest, yTest, tauz3[j-1]);
   // }
   // fclose(f3);


}


