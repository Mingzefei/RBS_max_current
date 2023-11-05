clear;clc;
outfile_path = sprintf('.\\main.out');
delete(outfile_path);
diary(outfile_path);

struct_list = {'f','e','e2f'};
num_b_list = [2,4,6];
method_list = {'Greedy','SA','GA'};

for i = 1:length(struct_list)
    id = struct_list{i};
    for j = 1:length(num_b_list)
        num_b = num_b_list(j);
        % create RBS
        if strcmp(id, 'f')
            rbs = RBSClass_f(num_b);
            str_id = [id,num2str(num_b)];
        elseif strcmp(id, 'e')
            rbs = RBSClass_e(num_b);
            str_id = [id,num2str(num_b)];
        elseif strcmp(id, 'e2f') && num_b == 2
            rbs = RBSClass_e2f1();
            str_id = 'e2f1';
        elseif strcmp(id, 'e2f') && num_b == 4
            rbs = RBSClass_e2f2();
            str_id = 'e2f2';
        elseif strcmp(id, 'e2f') && num_b == 6
            rbs = RBSClass_e2f3();
            str_id = 'e2f3';
        else
            continue
        end
        for k = 1:length(method_list)
            method = method_list{k}; 
            fprintf('Solve %s by %s\n',str_id, method)
            % solve RBS
            if strcmp(method, 'Greedy')
                [mac, x_s, num_iter, all_mac] = rbs.get_mac();
            elseif strcmp(method, 'SA')
                [mac, x_s, num_iter, all_mac] = rbs.get_mac_SA();
            elseif strcmp(method, 'GA')
                [mac, x_s, num_iter, all_mac] = rbs.get_mac_GA();
            end
            % print result
            fprintf('MAC: %.2f\n', mac)
            fprintf('num_iter: %d\n', num_iter)
            fid = fopen(sprintf('.\\%s-%s.txt',str_id,method),'w');
            fprintf(fid,'%g\n',all_mac);
            fclose(fid);
            [~,~,~,Io_ideal,Ib_ideal] = rbs.get_current(x_s);
            fprintf('Io_ideal: %s\n', Io_ideal)
            for battery=1:num_b
                fprintf('Ib_ideal(%d): %s\n',battery, Ib_ideal(battery))
            end
            fprintf('those switches are close: ')
            for l = 1:length(x_s)
                if (x_s(l)==1)
                    fprintf('%d ',l)
                end
            end
            fprintf('\n\n');
        end
    end
end
diary off;