%% basic setting
% take care : num_b, s_s, t_s

num_b = 3;
num_s = 3*num_b+1;
num_n = 2*num_b+4;

% edge: out
s_o = num_n;
t_o = 1;
weight_o = 10;

% edge: battery
s_b = 3:(3+num_b-1);
t_b = (3+num_b):(3+2*num_b-1);
weight_b = num_s*ones(1,num_b);

% edge: switch TODO:rewrite s_s and t_s
s_s = [1,2,2,2,3,4,6,7,8,9];
t_s = [2,3,4,5,7,8,9,9,9,10];
weight_s = ones(1,num_s);

%% graph model

% edge: total
s_total = [s_o, s_b, s_s, t_s];
t_total = [t_o, t_b, t_s, s_s];
weight_total = [weight_o, weight_b, weight_s, weight_s];
% G: total
G_total = digraph(s_total,t_total,weight_total);
node_pos=[0,0;1,0;1,1;2,1;3,1;1,2;2,2;3,2;1,3;0,3];
plot(G_total, ...
    'XData',node_pos(:,1), 'YData',node_pos(:,2), ...
    'EdgeLabel',G_total.Edges.Weight);
% get x_s
x_s = zeros(1,num_s);
list_of_s = [s_s', t_s'];
for i=1:num_b
    % get sp
    path1 = shortestpath(G_total,1,s_b(i));
    path2 = shortestpath(G_total,t_b(i),num_n);
    sp = [path1, path2];
    % set x_s
    for j=1:size(list_of_s,1)
        s = list_of_s(j,:);
        idx = ismember(sp,s);
        if any(idx) && any(abs(diff(find(idx))) == 1)
            x_s(j) = 1;
        end
    end
end

%% circuit model

% edge: degenerate
s_dege = [s_o, s_b, s_s];
t_dege = [t_o, t_b, t_s];
weight_dege = [weight_o, weight_b, weight_s];
% G and incidence: degenerate
G_dege = digraph(s_dege,t_dege,weight_dege);
node_pos=[0,0;1,0;1,1;2,1;3,1;1,2;2,2;3,2;1,3;0,3];
plot(G_dege, ...
    'XData',node_pos(:,1), 'YData',node_pos(:,2), ...
    'EdgeLabel',G_dege.Edges.Weight);
G_o = digraph(s_o,t_o,weight_o);
G_b = digraph(s_b,t_b,weight_b);
G_b = addnode(G_b,2); % add node 1 and end
G_s = digraph(s_s,t_s,weight_s);
Ao = full(-incidence(G_o));
Ao(end,:)=[];
Ab = full(-incidence(G_b));
Ab(end,:)=[];
As = full(-incidence(G_s));
As(end,:)=[];
A = [Ao, Ab, As];

Ro=sym('Ro','positive'); % for out
rb=sym('rb','positive'); % battery internal resistance
rs=sym('rs','positive'); % switch resistance
ub=sym('ub','positive'); % battery electric potential
x=diag(x_s);
Us=[0,-ub*ones(1,num_b),zeros(1,num_s)]';
Y=diag([1/Ro,ones(1,num_b)/rb,x_s/rs]);
Yn=A*Y*A';
Isn=A*Y*Us;
Un=Yn\Isn;
U=A'*Un;
I=Y*U-Y*Us;
Io=simplify(I(1));
Ib=simplify(I(2:num_b+1));
Io_ideal=subs(Io,rs,0);
Ib_ideal=subs(Ib,rs,0);
rate=Io_ideal/my_max(Ib_ideal);
disp(rate)

function m=my_max(list)
    m=list(1);
    for v = list(2:end)
        if isAlways(m<v)
            m=v;
        end
    end
end


