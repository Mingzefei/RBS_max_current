rbs = RBSClass_f(4);
rbs.plot_G_total
export_fig 'attachments\f4-gra.png' -transparent -m2
rbs.plot_G_dege
export_fig 'attachments\f4-dege.png' -transparent -m2
[mac, x_s] = rbs.get_mac();
rbs.plot_G_dege_hl_swithch(x_s)
export_fig 'attachments\f4-dege-mac.png' -transparent -m2