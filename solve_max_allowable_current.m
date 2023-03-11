Ao=sparse([1],[1],[-1],7,1);
Ab=sparse([3,4,5,6],[1,2,1,2],[1,1,-1,-1],7,2);
As=sparse([1,2,2,2,3,3,4,5,6,6,7,7,7],[1,1,2,3,2,4,3,5,4,6,5,6,7],[1,-1,1,1,-1,1,-1,1,-1,1,-1,-1,1]);
A=[Ao Ab As];
Nb=size(Ab,2); % batterys number
Ns=size(As,2); % switches number
Ro=sym('Ro','positive'); % for out
rb=sym('rb','positive'); % battery internal resistance
rs=sym('rs','positive'); % switch resistance
ub=sym('ub','positive'); % battery electric potential
switch_state=[0,1,1,1,1,1,0];
x=diag(switch_state);
Us=[0,-ub*ones(1,Nb),zeros(1,Ns)]';
Y=diag([1/Ro,ones(1,Nb)/rb,switch_state/rs]);
Yn=A*Y*A';
% det(Yn)
Isn=A*Y*Us;
Un=Yn\Isn;
U=A'*Un;
I=Y*U-Y*Us;
Io=simplify(I(1));
Ib=simplify(I(2:Nb+1));
Io_ideal=subs(Io,rs,0)
Ib_ideal=subs(Ib,rs,0)
rate=Io_ideal/my_max(Ib_ideal)

function m=my_max(list)
    m=list(1);
    for v = list(2:end)
        if isAlways(m<v)
            m=v;
        end
    end
end

