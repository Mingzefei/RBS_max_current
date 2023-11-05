classdef RBSClass_e2f3 < RBSClass
    properties
    end
    methods
        function rbs = RBSClass_e2f3()
            rbs = rbs@RBSClass(6);
            num_b = 6;
            rbs.num_b = num_b;
            rbs.num_s = 25;
            rbs.num_n = 22;
            % node: positon
            rbs.node_pos_x = [0,2,4,2,1,2,3,1,2,3,2,4,2,1,2,3,1,2,3,2,4,0];
            rbs.node_pos_y = [0,0,0,1,2,2,2,3,3,3,4,4,5,6,6,6,7,7,7,8,8,8];
  
            % edge: out
            rbs.s_o = rbs.num_n;
            rbs.t_o = 1;
            rbs.weight_o= 1+num_b*rbs.num_s+rbs.num_s;
            % edge: battery
            rbs.s_b = [5,6,7,14,15,16];
            rbs.t_b = [8,9,10,17,18,19];
            rbs.weight_b = rbs.num_s*ones(1,num_b);
            % edge: switch 
            rbs.s_s = [1,2,2,3,4,4,4,5,6,8,9,10,11,11,12,13,13,13,14,15,17,18,19,20,20];
            rbs.t_s = [2,3,4,12,5,6,7,9,10,11,11,11,12,13,21,14,15,16,18,19,20,20,20,21,22];
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
