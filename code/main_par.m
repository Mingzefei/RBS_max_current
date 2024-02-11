clear;clc;
outfile_path = sprintf('.\\main.out');
delete(outfile_path);
diary(outfile_path);

conditions = {'f',2,'Greedy'; 'f',2,'SA'; 'f',2,'GA';
    'f',4,'Greedy'; 'f',4,'SA'; 'f',4,'GA';
    'f',6,'Greedy'; 'f',6,'SA'; 'f',6,'GA';
    'e',2,'Greedy'; 'e',2,'SA'; 'e',2,'GA';
    'e',4,'Greedy'; 'e',4,'SA'; 'e',4,'GA';
    'e',6,'Greedy'; 'e',6,'SA'; 'e',6,'GA';
    'e2f',2,'Greedy'; 'e2f',2,'SA'; 'e2f',2,'GA';
    'e2f',4,'Greedy'; 'e2f',4,'SA'; 'e2f',4,'GA';
    'e2f',6,'Greedy'; 'e2f',6,'SA'; 'e2f',6,'GA'};

parfor i = 1:size(conditions,1)
    id = conditions{i,1};
    num_b = conditions{i,2};
    method = conditions{i,3};
    % create RBS
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
diary off;