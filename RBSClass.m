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
        Ro=sym('Ro','positive'); % for out
        rb=sym('rb','positive'); % battery internal resistance
        rs=sym('rs','positive'); % switch resistance
        ub=sym('ub','positive'); % battery electric potential
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
        function p=plot_G_total(rbs)
            p=plot(rbs.G_total, ...
                'XData',rbs.node_pos_x, 'YData',rbs.node_pos_y, ...
                'LineWidth',2,'EdgeColor','#666666', ...
                'MarkerSize',5);
            highlight(p,[rbs.num_n 1],'LineStyle','--')
            for node=1:length(rbs.s_b)
                highlight(p,[rbs.s_b(node),rbs.t_b(node)], ...
                    'EdgeColor','#006837','LineWidth',2);
            end
            axis off;
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
        function p=plot_G_dege(rbs)
            p=plot(rbs.G_dege, ...
                'XData',rbs.node_pos_x, 'YData',rbs.node_pos_y, ...
                'LineWidth',2,'EdgeColor','#666666', ...
                'MarkerSize',5);
            highlight(p,[rbs.num_n 1],'LineStyle','--')
            for node=1:length(rbs.s_b)
                highlight(p,[rbs.s_b(node),rbs.t_b(node)], ...
                    'EdgeColor','#006837','LineWidth',2);
            end
            axis off;
        end
        function p=plot_G_dege_hl_swithch(rbs,x_s)
            p=rbs.plot_G_dege;
            for i=1:length(x_s)
                if x_s(i)
                    highlight(p,[rbs.s_s(i),rbs.t_s(i)], ...
                        'EdgeColor','#e41a1c','LineWidth',2);
                end
            end
            axis off;
        end
%         function save_plot_dege(rbs,file_name)
%             saveas(rbs.plot_G_dege, file_name)
%         end
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
        function [out_current_ideal, ...
                isnot_short_circuit, ...
                Io_ideal,Ib_ideal]=get_current(rbs,x_s)

            Us=[0,-rbs.ub*ones(1,rbs.num_b),zeros(1,rbs.num_s)]';
            Y=diag([1/rbs.Ro,ones(1,rbs.num_b)/rbs.rb,x_s/rbs.rs]);
            Yn=rbs.A*Y*rbs.A';
            Isn=rbs.A*Y*Us;
            warning('off','all');
            Un=Yn\Isn;
            U=rbs.A'*Un;
            I=Y*U-Y*Us;
            Io=simplify(I(1));
            Ib=simplify(I(2:rbs.num_b+1));
            Io_ideal=subs(Io,rbs.rs,0);
            Ib_ideal=subs(Ib,rbs.rs,0);
            % whether battery short circuit
            isnot_short_circuit=1;
            for ib_ideal = Ib_ideal
                if ib_ideal == rbs.ub/rbs.rb
                    isnot_short_circuit=0;
                end
            end
            % out current
            if my_max(Ib) == 0
                out_current=0;
            else
                out_current=simplify(Io_ideal/my_max(Ib));
            end
            out_current_ideal=subs(out_current,rbs.rs,0);
        end
        function [mac_under_b,xs_mac] = get_mac_under_b(rbs, under_b)
            % count mac with given numbers(under_b) batteries
            all_choose = nchoosek(1:rbs.num_b, under_b);
            all_out_current_ideal = zeros(1,size(all_choose,1));
            all_isnot_short_circuit = ones(1,size(all_choose,1));
            for i = 1:size(all_choose,1)
                choose = all_choose(i,:);
                x_s = rbs.get_x_s(choose);
                [all_out_current_ideal(i), ...
                    all_isnot_short_circuit(i), ...
                    ]=rbs.get_current(x_s);
            end
            all_current = all_out_current_ideal .* all_isnot_short_circuit;
            mac_under_b = my_max(all_current);
            all_i_mac = find(all_current == mac_under_b); % index of mac
            xs_mac = rbs.get_x_s(all_choose(all_i_mac(1),:));
        end
        function [mac, xs] = get_mac(rbs)
            n_left = 1;
            n_right = rbs.num_b;
            while (n_left <= n_right)
                n_mid = fix((n_left + n_right) / 2);

                val_left = rbs.get_mac_under_b(n_left);
                val_mid = rbs.get_mac_under_b(n_mid);
                val_right = rbs.get_mac_under_b(n_right);

                if (val_left > val_mid)
                    n_right = n_mid - 1;
                elseif (val_right > val_mid)
                    n_left = n_mid + 1;
                else
                    n = n_mid;
                    [mac, xs] = rbs.get_mac_under_b(n);
                    return
                end
            end
            [mac, xs] = rbs.get_mac_under_b(n_left);
        end
    end
    methods (Static)
        function save_plot(p, file_name)
            saveas(p,file_name)
        end
        function save_fig(p, file_name)
            show(p);
            print(file_name,'-dpng','-r600')
        end
    end
end



function m=my_max(list)
    m=list(1);
    for i = 2:length(list)
        if isAlways(m<list(i))
            m=list(i);
        end
    end
end
