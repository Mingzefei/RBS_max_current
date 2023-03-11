function [is_battery_short_circuit, out_current_ideal] = max_allowable_current(switch_state,Ao,Ab,As)
% function out_current_ideal = max_allowable_current(switch_state,Ao,Ab,As)
%MAX_ALLOWABLE_CURRENT 此处显示有关此函数的摘要
% Ao=sparse([1],[1],[-1],7,1);
% Ab=sparse([3,4,5,6],[1,2,1,2],[1,1,-1,-1],7,2);
% As=sparse([1,2,2,2,3,3,4,5,6,6,7,7,7],[1,1,2,3,2,4,3,5,4,6,5,6,7],[1,-1,1,1,-1,1,-1,1,-1,1,-1,-1,1]);

Nb=size(Ab,2); % batterys number
Ns=size(As,2); % switches number
x=diag([1,ones(1,Nb),switch_state]); % state

% define resistance
Ro=sym('Ro','positive'); % for out
rb=sym('rb','positive'); % battery internal resistance
rs=sym('rs','positive'); % switch resistance
ub=sym('ub','positive'); % battery electric potential
% define A
A=[Ao,Ab,As];
% define Y and Yn
yo=1/Ro;
yb=ones(1,Nb)/rb;
ys=ones(1,Ns)/rs;
Y=diag([yo,yb,ys]);
Y=Y*x; % refine Y by x
Yn=A*Y*A';
% define Us
Us=[0;-ones(Nb,1)*ub;zeros(Ns,1)];
% define Is and Isn
Is=zeros(1+Nb+Ns,1);
Isn=A*Y*Us-A*Is;

% Yn
% det(Yn)
Un=Yn\Isn;
U=A'*Un;
I=Y*U-Y*Us+Is;

Io=simplify(I(1));
Ib=simplify(I(2:1+Nb));
Ib_ideal=subs(Ib,rs,0);
% whether battery short circuit
is_battery_short_circuit=0;
for ib_ideal = Ib_ideal
    if ib_ideal == ub/rb
        is_battery_short_circuit=1;
    end
end
% out current
if Ib_max == 0
    out_current=0;
else
    out_current=simplify(Io/max(Ib));
end
out_current_ideal=subs(out_current,rs,0);
end

