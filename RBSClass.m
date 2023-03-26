classdef RBSClass
    properties
        num_b
        num_s
        num_n
        node_pos_x
        node_pos_y
        s_o
        t_o
        weight_o
        s_b
        t_b
        weight_b
        s_s
        t_s
        weight_s
        G_total
        SPs
        G_dege
        A
    end
    methods
        function rbs = RBSClass(num_b)
            rbs.num_b = num_b;
            rbs.num_s = 3*num_b+1;
            rbs.num_n = 2*num_b+4;
            % node: positon
            rbs.node_pos_x = [0,1,1:num_b,1:num_b,1,0];
            rbs.node_pos_y = [0,0,ones(1,num_b),2*ones(1,num_b),3,3];
            % edge: out
            rbs.s_o = rbs.num_n;
            rbs.t_o = 1;
            rbs.weight_o= 1+num_b*rbs.num_s+rbs.num_s;
            % edge: battery
            rbs.s_b = 3:(3+num_b-1);
            rbs.t_b = (3+num_b):(3+2*num_b-1);
            rbs.weight_b = rbs.num_s*ones(1,num_b);
            % edge: switch 
            rbs.s_s = [1, 2*ones(1,num_b), ...
                3:1+num_b, ...
                3+num_b:2+2*num_b, ...
                rbs.num_n-1];
            rbs.t_s = [2, 3:2+num_b, ...
                4+num_b:2+2*num_b, ...
                (3+2*num_b)*ones(1,num_b), ...
                rbs.num_n];
            rbs.weight_s = ones(1,rbs.num_s);
            % G for graph
            rbs.G_total = rbs.get_G_total();
            % SPs
            rbs.SPs = rbs.get_SPs();
            % G for circuit
            rbs.G_dege = rbs.get_G_dege();
            % A
            rbs.A = rbs.get_A();
        end
        function G_total = get_G_total(rbs)
            s_total = [rbs.s_o, rbs.s_b, rbs.s_s, rbs.t_s];
            t_total = [rbs.t_o, rbs.t_b, rbs.t_s, rbs.s_s];
            weight_total = [rbs.weight_o, ...
                rbs.weight_b, ...
                rbs.weight_s, ...
                rbs.weight_s];
            G_total = digraph(s_total,t_total,weight_total);
        end
        function plot_G_total(rbs)
            plot(rbs.G_total, ...
                'XData',rbs.node_pos_x, 'YData',rbs.node_pos_y, ...
                'EdgeLabel',rbs.G_total.Edges.Weight);
        end
        function SPs = get_SPs(rbs)
            SPs = cell(rbs.num_b,1);
            for battery=1:rbs.num_b
                path1 = shortestpath(rbs.G_total,1,rbs.s_b(battery));
                path2 = shortestpath(rbs.G_total,rbs.t_b(battery),rbs.num_n);
                sp = [path1, path2];
                SPs{battery} = sp;
            end
        end
        function x_s = get_x_s(rbs,list_of_batteries)
            x_s = zeros(1,rbs.num_s);
            list_of_s = [rbs.s_s', rbs.t_s'];
            for battery=list_of_batteries
                sp = rbs.SPs{battery};
                % set x_s
                for j=1:size(list_of_s,1)
                    s = list_of_s(j,:);
                    idx = ismember(sp,s);
                    if any(idx) && any(abs(diff(find(idx))) == 1)
                        x_s(j) = 1;
                    end
                end
            end
        end
        function G_dege = get_G_dege(rbs)
            s_dege = [rbs.s_o, rbs.s_b, rbs.s_s];
            t_dege = [rbs.t_o, rbs.t_b, rbs.t_s];
            weight_dege = [rbs.weight_o, rbs.weight_b, rbs.weight_s];
            G_dege = digraph(s_dege,t_dege,weight_dege);
        end
        function plot_G_dege(rbs)
            plot(rbs.G_dege, ...
                'XData',rbs.node_pos_x, 'YData',rbs.node_pos_y, ...
                'EdgeLabel',rbs.G_dege.Edges.Weight);
        end
        function A = get_A(rbs)
            G_o = digraph(rbs.s_o,rbs.t_o,rbs.weight_o);
            Ao = full(-incidence(G_o));
            Ao(end,:)=[];
            G_b = digraph(rbs.s_b,rbs.t_b,rbs.weight_b);
            G_b = addnode(G_b, numnodes(G_o)-numnodes(G_b));
            Ab = full(-incidence(G_b));
            Ab(end,:)=[];
            G_s = digraph(rbs.s_s,rbs.t_s,rbs.weight_s);
            G_s = addnode(G_s, numnodes(G_o)-numnodes(G_s));
            As = full(-incidence(G_s));
            As(end,:)=[];
            A = [Ao, Ab, As];
        end
        function [Io_ideal, Ib_ideal, rate]=get_current(rbs,x_s)
            Ro=sym('Ro','positive'); % for out
            rb=sym('rb','positive'); % battery internal resistance
            rs=sym('rs','positive'); % switch resistance
            ub=sym('ub','positive'); % battery electric potential
            Us=[0,-ub*ones(1,rbs.num_b),zeros(1,rbs.num_s)]';
            Y=diag([1/Ro,ones(1,rbs.num_b)/rb,x_s/rs]);
            Yn=rbs.A*Y*rbs.A';
            Isn=rbs.A*Y*Us;
            Un=Yn\Isn;
            U=rbs.A'*Un;
            I=Y*U-Y*Us;
            Io=simplify(I(1));
            Ib=simplify(I(2:rbs.num_b+1));
            Io_ideal=subs(Io,rs,0);
            Ib_ideal=subs(Ib,rs,0);
            rate=Io_ideal/my_max(Ib_ideal);
        end
    end
end



function m=my_max(list)
    m=list(1);
    for v = list(2:end)
        if isAlways(m<v)
            m=v;
        end
    end
end
