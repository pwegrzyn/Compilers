# control flow instruction

A = [[1,2,3], [1,4,5]];

A[1,2];

B = ones(5);

tmp = B[2,1];

print tmp/2;

x= 1;
zeros(x);


N = 10;
M = 20;
for i = 1:N {
    g = 1;
    for j = i:M {
        print i, j;
        print g;
    }
}

k = 1;
while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;   
    
    k = k - 1;
}


