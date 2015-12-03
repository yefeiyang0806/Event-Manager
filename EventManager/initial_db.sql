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

INSERT INTO resource_type VALUES ('30f6a174-9811-11e5-8f4a-402cf4f6ef0c', 'Show Floor', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO resource_type VALUES ('6e5e1c2c-9811-11e5-a4f0-402cf4f6ef0c', 'S.Ballroom', '2015/11/30', '14:58:00', 'Feiyang');
INSERT INTO resource_type VALUES ('767f99a8-9811-11e5-b83b-402cf4f6ef0c', 'L.Ballroom', '2015/11/30', '14:58:00', 'Feiyang');

INSERT INTO resource VALUES ('4245b22e-989a-11e5-99f8-402cf4f6ef0c', 'SF-101', 'SF-101', 'Share Floor space 1', 15, '2015/11/30', '14:58:00', 'Feiyang', '30f6a174-9811-11e5-8f4a-402cf4f6ef0c');
INSERT INTO resource VALUES ('a2c3c030-989a-11e5-a5c9-402cf4f6ef0c', 'SF-102', 'SF-102', 'Share Floor space 2', 15, '2015/11/30', '14:58:00', 'Feiyang', '30f6a174-9811-11e5-8f4a-402cf4f6ef0c');
INSERT INTO resource VALUES ('c918d418-989a-11e5-b267-402cf4f6ef0c', 'SBrm-01', 'SBrm-01', 'Small Ballroom 01', 30, '2015/11/30', '14:58:00', 'Feiyang', '6e5e1c2c-9811-11e5-a4f0-402cf4f6ef0c');
INSERT INTO resource VALUES ('11a2f6da-989b-11e5-87c7-402cf4f6ef0c', 'LBrm-02', 'LBrm-02', 'Large Ballroom 02', 100, '2015/11/30', '14:58:00', 'Feiyang', '767f99a8-9811-11e5-b83b-402cf4f6ef0c');