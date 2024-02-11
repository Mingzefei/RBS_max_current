classdef RBSClass_e2f2 < RBSClass
    properties
    end
    methods
        function rbs = RBSClass_e2f2()
            rbs = rbs@RBSClass(4);
            num_b = 4;
            rbs.num_b = num_b;
            rbs.num_s = 19;
            rbs.num_n = 18;
            % node: positon
            rbs.node_pos_x = [0,2,4,2,1,3,1,3,2,4,2,1,3,1,3,2,4,0];
            rbs.node_pos_y = [0,0,0,1,2,2,3,3,4,4,5,6,6,7,7,8,8,8];
  
            % edge: out
            rbs.s_o = rbs.num_n;
            rbs.t_o = 1;
            rbs.weight_o= 1+num_b*rbs.num_s+rbs.num_s;
            % edge: battery
            rbs.s_b = [5,6,12,13];
            rbs.t_b = [7,8,14,15];
            rbs.weight_b = rbs.num_s*ones(1,num_b);
            % edge: switch 
            rbs.s_s = [1,2,2,3,4,4,5,7,8,9,9,10,11,11,12,14,15,16,16];
            rbs.t_s = [2,3,4,10,5,6,8,9,9,10,11,17,12,13,15,16,16,17,18];
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
