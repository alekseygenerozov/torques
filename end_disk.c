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
#define MAX_SIZE 1000



// void heartbeat(struct reb_simulation* const r);
struct tup
{
	double sum;
	double c;
};

struct tup comp_sum(double sum,  double val, double c){
    struct tup res;
    double yy=val-c;
    double tt=sum+yy;
    res.c=(tt-sum)-yy;
    res.sum= tt;

    return res;
}

void out(char* pre, char* tag, double out){
    char fname[80]="";
    strcat(fname, pre);
    strcat(fname, "_");
    strcat(fname, tag);
    FILE* f = fopen(fname, "w");
    fprintf(f, "%0.10e\n", out);
    fclose(f);

}

int main(int argc, char* argv[]){
    struct reb_simulation* r = reb_create_simulation();
    r->G         = 1;
    const double e_test =atof(argv[1]);
    const double a_test = atof(argv[2]);
    const double ang_test = atof(argv[3]);
    const double ang_test_rad=ang_test*M_PI/180;
    printf("%lf\n", e_test);
    char line[MAX_SIZE];
    int N=0;

    int offset = atoi(argv[5]);
    char* tag="a";
    if (offset!=0){
    	tag="b";
    	offset=1;
    }
 		   
    const int bins = atoi(argv[6]);
    const double m = 1.0/4e6/bins;
    // const int N =1000;
    // const double tau0 = pow(N, 0.5)*pow(m*bins, 2)/a_test;
    printf("%d\n", N);

    // Initial conditions
    struct reb_particle star = {0};
    star.m = 1;
    reb_add(r, star);


    // double* a =malloc(N*sizeof(double));
    char aa[80]="";
    strcat(aa, "a_");
    strcat(aa, argv[4]);
    strcat(aa, ".txt");
    FILE* AA = fopen(aa, "r");
    FILE* AA2= fopen(aa, "r");


    char oo[80]="";
    strcat(oo, "Om_");
    strcat(oo, argv[4]);
    strcat(oo, ".txt");
    FILE* OM = fopen(oo, "r");

    char oo2[80]="";
    strcat(oo2, "om_");
    strcat(oo2, argv[4]);
    strcat(oo2, ".txt");
    FILE* OM2 = fopen(oo2, "r");


    char ii[80]="";
    strcat(ii, "inc_");
    strcat(ii, argv[4]);
    strcat(ii, ".txt");
    FILE* INC = fopen(ii, "r");
    double a, e, inc, omega, Omega, M;
    printf("%lf\n", atof(argv[1]));


    while((fgets(line, sizeof(line), AA2) != NULL) && (N<MAX_SIZE)){
        e=0.7;
        N+=1;        
        fscanf(AA, "%lf", &a);
        fscanf(OM, "%lf", &Omega);
        // printf("%d\n", N);
        fscanf(OM2, "%lf", &omega);
        fscanf(INC, "%lf", &inc);

        // printf("%lf %lf %lf %lf\n", a, inc, Omega, omega);


        for (int j=0; j<bins; j++){
            struct reb_particle pt;
            M = (j+0.5*offset)*((2.*M_PI)/(double)bins);
            double f = reb_tools_M_to_f(e, M);
            pt = reb_tools_orbit_to_particle(r->G, r->particles[0], m, a, e, inc, Omega, omega, f);
            reb_add(r, pt);
        }
        // printf("%d\n", N);


    }
    printf("%d\n", N);

    fclose(AA);
    fclose(OM);
    fclose(OM2);
    fclose(INC);


    double* farr=malloc(bins*sizeof(double));
    for (int j=0; j<bins; j++){
        struct reb_particle pt;
        double M = (j+0.5*offset)*((2.*M_PI)/(double)bins);
        double f = reb_tools_M_to_f(e_test, M);
        pt = reb_tools_orbit2d_to_particle(r->G, r->particles[0], m, a_test, e_test, ang_test*M_PI/180, f);

        reb_add(r, pt);
        farr[j]=f;

    }


	// double ex=e_test*cos(ang_test*M_PI/180);
 	//double ey=e_test*sin(ang_test*M_PI/180);
   	// double* tauz2 = malloc(bins*sizeof(double));
   	// double* tauz3 = malloc(bins*sizeof(double));

    double c = 0;
    // double c1 = 0;
    double c2 = 0;
    double c3 = 0;

    double forcexTot=0;
    double forceyTot=0;
    double forcezTot=0;

    double taux=0;
    double tauy=0;
    double tauz=0;
    double tauzTot=0;
    // double edotx=0;
    // double edoty=0;
    double jz=0;
    double ieDot=0;
    double ieDot2=0;
    // double ieDot3=0;
    double pre=1.0;
    double tmp=0;
    struct tup res;

    printf("%lf\n", r->particles[N*bins].x);

    for (int i=1; i<N*bins+1; i++){
        double x=r->particles[i].x;
        double y=r->particles[i].y;
        double z=r->particles[i].z;

        for (int j=1; j<bins+1; j++){
           // if (i==1){
           //     tauz2[j]=0;
           // }
           // if (j==1){
           //     tauz3[i-1]=0;
           // }
            double xTest=r->particles[N*bins+j].x;
            double yTest=r->particles[N*bins+j].y;
            double zTest=r->particles[N*bins+j].z;
            double vx=r->particles[N*bins+j].vx;
            double vy=r->particles[N*bins+j].vy;
            double vz=r->particles[N*bins+j].vz;
            //Planar orbit
            vz=0;
            double phi = farr[j-1];



            double d=pow(pow(x-xTest, 2.)+pow(y-yTest,2.)+pow(z-zTest,2.),0.5);
            double forcex = -pow(m,2.0)/pow(d,3.0)*(xTest-x);
            double forcey = -pow(m,2.0)/pow(d,3.0)*(yTest-y);
            double forcez = -pow(m,2.0)/pow(d,3.0)*(zTest-z);

            forcexTot+=forcex;
            forceyTot+=forcey;
            forcezTot+=forcez;

            taux= (yTest*forcez-zTest*forcey);
            tauy= -(xTest*forcez-zTest*forcex);
            tauz= (xTest*forcey-yTest*forcex);

            // tauzTot+=tauz;
            res=comp_sum(tauzTot, tauz, c);
            c=res.c;
            tauzTot=res.sum;
            //Angular momentum of test orbit--Take this to be in the xy plane
            jz = xTest*vy-yTest*vx;
            double fr=forcex*cos(phi+ang_test_rad)+forcey*sin(phi+ang_test_rad);
            double vr=vx*cos(phi+ang_test_rad)+vy*sin(phi+ang_test_rad);

            tmp = pre*(-jz*fr/e_test*(cos(phi)));
            res=comp_sum(ieDot2, tmp, c2);
            c2=res.c;
            ieDot2=res.sum;

            tmp = pre*(-jz*fr/e_test*(cos(phi))+tauz*vr/e_test*(2/e_test+cos(phi)));
            res=comp_sum(ieDot, tmp, c3);
            c3=res.c;
            ieDot=res.sum;


       }

    }
    // double ieDot=(ex*edoty-ey*edotx)/pow(e_test, 2.);

    char tag2[80]="";
    strcat(tag2, "N");
    snprintf(tag2+strlen(tag2), sizeof(tag2), "%d", N);
    strcat(tag2,"_");
    strcat(tag2, tag);
    for (int i=1; i<5; i++){
        strcat(tag2, "_");
        strcat(tag2, argv[i]);
    }
    printf("%s\n",tag2);

    out("tau", tag2, tauzTot);
    out("i", tag2, ieDot);
    out("i2", tag2, ieDot2);

    // char iname[80]="";
    // strcat(iname, "i_N");
    // snprintf(iname+strlen(iname), sizeof(iname), "%d", N);
    // strcat(iname,"_");
    // strcat(iname, tag);
    // for (int i=1; i<5; i++){
    //     strcat(iname, "_");
    //     strcat(iname, argv[i]);
    // }
    // printf("%s\n",iname);
    // FILE *ie=fopen(iname, "w");
    // fprintf(ie, "%0.10e\n", ieDot2);
    // fclose(ie);

    return 0;
}


