include "alldifferent.mzn";
int: n;  % Número de equipos
int: Min;  % Tamaño mínimo de las giras y permanencias
int: Max;  % Tamaño máximo de las giras y permanencias

% Variables de decisión
array[1..2*(n-1), 1..n] of var -n..n: Cal;  % Matriz Calendario

% Matriz de distancias
array[1..n, 1..n] of int: D;



% Variable para la suma del costo de las distancias
var int: totalDistance;

% Un equipo no puede jugar contra si mismo
constraint forall(i in 1..2*(n-1), j in 1..n) (
  Cal[i, j] != -j /\ Cal[i, j] != j
);

%en ninguna fila pueden haber numeros repetidos
constraint forall(i in 1..2*(n-1)) (
  forall(j in 1..n, k in j+1..n) (
    abs(Cal[i, j]) != abs(Cal[i, k])
  )
);

% Todas las filas tienen que tener valores diferentes
constraint forall(j in 1..n) (
  alldifferent([Cal[i, j] | i in 1..2*(n-1)])
);


% Todas las columnas tienen que tener valores diferentes
constraint forall(i in 1..2*(n-1)) (
  alldifferent([Cal[i, j] | j in 1..n])
);

% Giras y permanencias minimas y maximas
constraint forall(j in 1..n, i in 1..(2*(n-1)-Max)) (
  let {
    var int: consecutivePos = sum(k in i..(i + Max)) (bool2int(Cal[k, j] > 0));
    var int: consecutiveNeg = sum(k in i..(i + Max)) (bool2int(Cal[k, j] < 0))
  } in
  (consecutivePos >= Min /\ consecutivePos <= Max) /\ (consecutiveNeg >= Min /\ consecutiveNeg <= Max)
);

% Restriccion partidos de seguido
constraint forall(i in 2..2*(n-1), j in 1..n) (
    abs(Cal[i-1, j]) != abs(Cal[i, j])
);

% Restricción
/*constraint forall(j in 1..n, k in 1..n where k != j) (
    exists(i1 in 1..2*(n-1), i2 in 1..2*(n-1) where i1 != i2) (
        (abs(Cal[i1, j]) = k /\ Cal[i2, j] = -k)
    )
);*/

constraint sum(j in 1..n) (
                 exists(i in 1..2*(n-1)-Max) (
                      sum(k in i..(i + Max)) (bool2int(Cal[k, j] < 0)) >= Max - 1 
                 )
          ) >= n/2;


constraint forall(i in 1..2*(n-1), j in 1..n) (
  exists(k in 1..n) (
    (Cal[i, j] == k /\ Cal[i, k] == -j)\/(Cal[i, k] == j /\ Cal[i, j] == -k)
  )
);

% Restricciones de tamaño de giras y permanencias
% Restricción de no repetición de partidos en fechas consecutivas

% Cálculo de la suma del costo de las distancias
totalDistance = sum(i in 1..2*(n-1), j in 1..n) (
    let {
        var int: value = if i == 1 /\ Cal[i,j] > 0 then 0 %Primera fecha y me toca de local
                         elseif i == 1 /\ Cal[i,j] < 0 then D[j, abs(Cal[i, j])] %Primera fecha y me toca de visitante
                         elseif i == 2*(n-1) /\ Cal[i-1, j] < 0 /\ Cal[i,j] < 0 then D[abs(Cal[i-1, j]), abs(Cal[i, j])]+D[abs(Cal[i,j]),j] %Anterior fecha estaba de visitante, ahora visitante y es la ultima fecha
                         elseif i == 2*(n-1) /\ Cal[i-1, j] > 0 /\ Cal[i, j] < 0 then D[j, abs(Cal[i, j])]+D[abs(Cal[i,j]),j] %Si mi anterior fecha estaba de local y ahora de visitante y es la ultima fecha
                         elseif i > 1 /\ Cal[i-1, j] < 0 /\ Cal[i,j] < 0 then D[abs(Cal[i-1, j]), abs(Cal[i, j])] %Si mi anterior fecha estaba de visitante y ahora de visitante 
                         elseif i > 1 /\ Cal[i-1, j] < 0 /\ Cal[i,j] > 0 then D[abs(Cal[i-1, j]), j] %Si mi anterior fecha estaba de visitante y ahora de local
                         elseif i > 1 /\ Cal[i-1, j] > 0 /\ Cal[i, j] > 0 then 0 %Si mi anterior fecha estaba de local y ahora me toca de local
                         elseif i > 1 /\ Cal[i-1, j] > 0 /\ Cal[i, j] < 0 then D[j, abs(Cal[i, j])] %Si mi anterior fecha estaba de local y ahora de visitante                      
                         else 0 endif;
                         
                   
    } in value
);


% Meta: Minimizar la distancia total de las giras
%solve satisfy;
solve minimize totalDistance;