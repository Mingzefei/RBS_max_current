classdef RBSClass_e2f1 < RBSClass
    properties
    end
    methods
        function rbs = RBSClass_e2f1()
            rbs = rbs@RBSClass(2);
            num_b = 2;
            rbs.num_b = num_b;
            rbs.num_s = 13;
            rbs.num_n = 14;
            % node: positon
            rbs.node_pos_x = [0,1,2,1,1,1,1,2,1,1,1,1,2,0];
            rbs.node_pos_y = [0,0,0,1,2,3,4,4,5,6,7,8,8,8];
  
            % edge: out
            rbs.s_o = rbs.num_n;
            rbs.t_o = 1;
            rbs.weight_o= 1+num_b*rbs.num_s+rbs.num_s;
            % edge: battery
            rbs.s_b = [5,10];
            rbs.t_b = [6,11];
            rbs.weight_b = rbs.num_s*ones(1,num_b);
            % edge: switch 
            rbs.s_s = [1,2,2,3,4,6,7,7,8,9,11,12,12];
            rbs.t_s = [2,3,4,8,5,7,8,9,13,10,12,13,14];
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
