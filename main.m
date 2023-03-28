delete main.out
diary('main.out');
%% RBS-f
for i = [2,4,6,8]
    % 创建RBSClass_f对象
    rbs_f = RBSClass_f(i);
    % 绘制并保存对象结构
    path_file = sprintf('.\\attachments\\f-dege-%d.png',i);
    rbs_f.save_plot(rbs_f.plot_G_dege(),path_file)
    % 获取MAC和x_s并打印相关信息
    [mac, x_s] = rbs_f.get_mac();
    fprintf('MAC of RBS_f(%d): %.2f\n', i, mac)
    [~,~,Io_ideal,Ib_ideal] = rbs_f.get_current(x_s);
    fprintf('Io_ideal: %s\n', Io_ideal)
    for battery=1:i
        fprintf('Ib_ideal(%d): %s\n',battery, Ib_ideal(battery))
    end
    fprintf('those switches are close: ')
    for j = 1:length(x_s)
        if (x_s(j)==1)
            fprintf('%d ',j)
        end
    end
    fprintf('\n\n');
    % 绘制并保存结果
    path_file = sprintf('.\\attachments\\f-dege-mac-%d.png',i);
    rbs_f.save_plot(rbs_f.plot_G_dege_hl_swithch(x_s),path_file)
end

%% RBS-e
for i = 2:4
    % 创建RBSClass_e对象
    rbs_e = RBSClass_e(i);
    % 绘制并保存对象结构
    path_file = sprintf('.\\attachments\\e-dege-%d.png',i);
    rbs_e.save_plot(rbs_e.plot_G_dege(),path_file)
    % 获取MAC和x_s并打印相关信息
    [mac, x_s] = rbs_e.get_mac();
    fprintf('MAC of RBS_e(%d): %.2f\n', i, mac)
    [~,~,Io_ideal,Ib_ideal] = rbs_e.get_current(x_s);
    fprintf('Io_ideal: %s\n', Io_ideal)
    for battery=1:i
        fprintf('Ib_ideal(%d): %s\n',battery, Ib_ideal(battery))
    end
    fprintf('those switches are close: ')
    for j = 1:length(x_s)
        if (x_s(j)==1)
            fprintf('%d ',j)
        end
    end
    fprintf('\n\n');
    % 绘制并保存结果
    path_file = sprintf('.\\attachments\\e-dege-mac-%d.png',i);
    rbs_e.save_plot(rbs_e.plot_G_dege_hl_swithch(x_s),path_file)
end

%% RBS-e2f2
rbs_e2f2 = RBSClass_e2f2();
path_file = sprintf('.\\attachments\\e2f2-dege.png');
rbs_e2f2.save_plot(rbs_e2f2.plot_G_dege(),path_file)
[mac, x_s] = rbs_e2f2.get_mac();
fprintf('MAC of RBS_e2f2: %.2f\n', mac)
[~,~,Io_ideal,Ib_ideal] = rbs_e2f2.get_current(x_s);
fprintf('Io_ideal: %s\n', Io_ideal)
for battery=1:i
    fprintf('Ib_ideal(%d): %s\n',battery, Ib_ideal(battery))
end
fprintf('those switches are close: ')
for j = 1:length(x_s)
    if (x_s(j)==1)
        fprintf('%d ',j)
    end
end
fprintf('\n\n');
path_file = sprintf('.\\attachments\\e2f2-dege-mac.png');
rbs_e2f2.save_plot(rbs_e2f2.plot_G_dege_hl_swithch(x_s),path_file)

diary off;