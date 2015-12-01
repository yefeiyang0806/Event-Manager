INSERT INTO role VALUES ('fa3b4e76-972c-11e5-80b0-402cf4f6ef0c', 'normal', 'default role for testing', '2015/11/30', '14:39:00', 'Feiyang');
INSERT INTO role VALUES ('5f2857c0-972d-11e5-be6e-402cf4f6ef0c', 'admin', 'Admin role for testing', '2015/11/30', '14:40:00', 'Feiyang');

INSERT INTO menu VALUES ('930db3d2-972d-11e5-b3b8-402cf4f6ef0c', 'Event Management', 'Menu/Event Management');
INSERT INTO menu VALUES ('e3f18738-972d-11e5-ba3e-402cf4f6ef0c', 'Role Management', 'Menu/Role Management');

INSERT INTO role_menu VALUES ('1eca3a58-972e-11e5-be27-402cf4f6ef0c', 'fa3b4e76-972c-11e5-80b0-402cf4f6ef0c', '930db3d2-972d-11e5-b3b8-402cf4f6ef0c');
INSERT INTO role_menu VALUES ('0a798ba2-972f-11e5-b8e3-402cf4f6ef0c', 'fa3b4e76-972c-11e5-80b0-402cf4f6ef0c', 'e3f18738-972d-11e5-ba3e-402cf4f6ef0c');
INSERT INTO role_menu VALUES ('5be30f5a-972e-11e5-94e5-402cf4f6ef0c', '5f2857c0-972d-11e5-be6e-402cf4f6ef0c', 'e3f18738-972d-11e5-ba3e-402cf4f6ef0c');
INSERT INTO role_menu VALUES ('7cf5a43a-972e-11e5-9414-402cf4f6ef0c', '5f2857c0-972d-11e5-be6e-402cf4f6ef0c', '930db3d2-972d-11e5-b3b8-402cf4f6ef0c');

INSERT INTO content VALUES ('564b518c-972f-11e5-a06b-402cf4f6ef0c', 'HANA', 'HANA', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO content VALUES ('7756b948-972f-11e5-86db-402cf4f6ef0c', 'Cloud', 'Cloud', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO content VALUES ('81066722-972f-11e5-bea0-402cf4f6ef0c', 'Fiori', 'Fiori', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO content VALUES ('89c78aba-972f-11e5-bc7b-402cf4f6ef0c', 'ABAP', 'ABAP', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO content VALUES ('91ea1528-972f-11e5-a718-402cf4f6ef0c', 'IOT', 'IOT', '2015/11/30', '14:58:00', 'Feiyang');

INSERT INTO `format` VALUES ('142cd428-9730-11e5-b88e-402cf4f6ef0c', 'Developer Fair', 'Developer Fair', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO `format` VALUES ('2dcc9e9c-9733-11e5-859e-402cf4f6ef0c', 'Downtown Block', 'Downtown Block', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO `format` VALUES ('37dd3f40-9733-11e5-a857-402cf4f6ef0c', 'SAP Talk', 'SAP Talk', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO `format` VALUES ('40a65be6-9733-11e5-b5ba-402cf4f6ef0c', 'Customer Talk', 'Customer Talk', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO `format` VALUES ('4a3ab8d4-9733-11e5-92fb-402cf4f6ef0c', 'Innovative Zone', 'Innovative Zone', '2015/11/30', '14:58:00', 'Feiyang');