classdef RBSClass_f < RBSClass
    properties
    end
    methods
        function rbs = RBSClass_f(num_b)
            rbs = rbs@RBSClass(num_b);
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
    end
end
