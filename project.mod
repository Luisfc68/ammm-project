int             K = ...;
int 	  P[1..K] = ...;
int 	  R[1..K] = ...;
int 	  A[1..K] = ...;
int 	  C[1..K] = ...;

int             N = ...;
int M[1..N][1..N] = ...;

int D = 7;
int MA = 6;

// Auxiliar variables
int M50[1..K][1..N][1..N];
int prev_day[d in 1..D] = (d==1 ? D : d-1);
int next_day[d in 1..D] = (d==D ? 1 : d+1);
int MaxCap[k in 1..K] = (7 * A[k]) div (A[k] + 1);

// A camera of model k is installed at crossing n
dvar boolean x_nk[1..N][1..K];
// A camera of model k is on at crossing n at day d
dvar boolean y_nkd[1..N][1..K][1..D];

execute {
  for (var k = 1; k <= K; ++k)
  	for (var i = 1; i <= N; ++i)
  		for (var j = 1; j <= N; ++j)
  			M50[k][i][j] = R[k] >= M[i][j];
}

minimize (sum(n in 1..N) sum(k in 1..K) P[k] * x_nk[n][k]) + 
         (sum(n in 1..N) sum(k in 1..K) sum(d in 1..D) C[k] * y_nkd[n][k][d]); 

subject to {
    // Only one camera per crossing
    forall(n in 1..N)
      sum(k in 1..K) x_nk[n][k] <= 1;
      
    // A camera can only be turned on if it is actually installed
    forall(n in 1..N, k in 1..K, d in 1..D)
      y_nkd[n][k][d] <= x_nk[n][k];
          
    // Every crossing j must be watched every day
    forall(j in 1..N, d in 1..D)
      sum(n in 1..N) sum(k in 1..K) M50[k][n][j] * y_nkd[n][k][d] >= 1;
    
    // A camera must work at least 2 days after starting
    forall(n in 1..N, k in 1..K, d in 1..D)
      y_nkd[n][k][d] - y_nkd[n][k][prev_day[d]] <= y_nkd[n][k][next_day[d]];
      
    // A camera must respect its autonomy
    forall(n in 1..N, k in 1..K, d in 1..D)
      sum(t in 0..A[k]) y_nkd[n][k][((d+t-1)%D)+1] <= A[k];
      
    // The total supply of days from installed cameras must equal or
    // exceed the demand of 7 days
    forall(j in 1..N)
       sum(n in 1..N) sum(k in 1..K) M50[k][n][j] * MaxCap[k] * x_nk[n][k] >= D;
}