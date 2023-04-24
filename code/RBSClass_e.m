classdef RBSClass_e < RBSClass
    properties
    end
    methods
        function rbs = RBSClass_e(num_b)
            rbs = rbs@RBSClass(num_b);
            rbs.num_b = num_b;
            rbs.num_s = 3*num_b+3;
            rbs.num_n = 3*num_b+4;
            % node: positon
            rbs.node_pos_x = [0,repmat([1,2,1],1,num_b),1,2,0];
            i = 1:num_b;
            temp = reshape([2*i-2; 2*i-2; 2*i-1], 1, []);
            rbs.node_pos_y = [0,temp,temp(end)+1,temp(end)+1,temp(end)+1];
  
            % edge: out
            rbs.s_o = rbs.num_n;
            rbs.t_o = 1;
            rbs.weight_o= 1+num_b*rbs.num_s+rbs.num_s;
            % edge: battery
            rbs.s_b = 4:3:(3*num_b+1);
            rbs.t_b = 5:3:(3*num_b+2);
            rbs.weight_b = rbs.num_s*ones(1,num_b);
            % edge: switch 
            i = 1:num_b;
            temp = reshape([3*i-1; 3*i-1; 3*i], 1, []);
            rbs.s_s = [1, temp, temp(end)+2, temp(end)+2];
            temp = reshape([3*i; 3*i+1; 3*i+3], 1, []);
            rbs.t_s = [2, temp, temp(end), temp(end)+1];
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
