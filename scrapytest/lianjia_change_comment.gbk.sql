USE scrapy;
alter table lianjia_house change column id id varchar(32) comment '���ұ��';
alter table lianjia_house change column layout layout varchar(256) NOT NULL COMMENT '����';
alter table lianjia_house change column floor floor varchar(128) NOT NULL COMMENT '¥��';
alter table lianjia_house change column total_area total_area varchar(256) NOT NULL DEFAULT '' COMMENT '�������';
alter table lianjia_house change column layout_structure layout_structure varchar(256) NOT NULL DEFAULT '' COMMENT '��ʽ��ƽ��';
alter table lianjia_house change column usable_area usable_area varchar(256) NOT NULL DEFAULT '' COMMENT '�������';
alter table lianjia_house change column build_type build_type varchar(32) NOT NULL DEFAULT '' COMMENT '��¥';
alter table lianjia_house change column orientation orientation varchar(32) NOT NULL DEFAULT '' COMMENT '����';
alter table lianjia_house change column construction_year construction_year year NOT NULL DEFAULT '0000' COMMENT '�������';
alter table lianjia_house change column decoration decoration varchar(32) NOT NULL DEFAULT '' COMMENT '��װ';
alter table lianjia_house change column build_structure build_structure varchar(64) NOT NULL DEFAULT '' COMMENT 'ש�졢�ֻ�';
alter table lianjia_house change column heating_mode heating_mode varchar(64) NOT NULL DEFAULT '' COMMENT '����ģʽ';
alter table lianjia_house change column hshold_ladder_ratio hshold_ladder_ratio varchar(128) NOT NULL DEFAULT '' COMMENT '�ݻ���';
alter table lianjia_house change column property_right_length property_right_length varchar(64) NOT NULL DEFAULT '' COMMENT '��Ȩ����';
alter table lianjia_house change column elevator elevator varchar(16) NOT NULL DEFAULT '' COMMENT '���޵���';
alter table lianjia_house change column water_type water_type varchar(16) NOT NULL DEFAULT '' COMMENT '��ˮ����';
alter table lianjia_house change column electric_type electric_type varchar(16) NOT NULL DEFAULT '' COMMENT '�õ�����';
alter table lianjia_house change column gas_price gas_price varchar(16) NOT NULL DEFAULT '' COMMENT 'ȼ���۸�';
alter table lianjia_house change column trans_right trans_right varchar(64) NOT NULL DEFAULT '' COMMENT '��Ʒ�����������÷�';
alter table lianjia_house change column house_property house_property varchar(256) NOT NULL DEFAULT '' COMMENT '��Ԣ';
alter table lianjia_house change column ownership_type ownership_type varchar(32) NOT NULL DEFAULT '' COMMENT '�ǹ���';
alter table lianjia_house change column community community varchar(32) NOT NULL DEFAULT '' COMMENT 'С����';
alter table lianjia_house change column district district varchar(64) NOT NULL DEFAULT '' COMMENT '����';
alter table lianjia_house change column business_district business_district varchar(128) NOT NULL DEFAULT '' COMMENT '��Ȧ';
alter table lianjia_house change column crawl_unit crawl_unit varchar(64) NOT NULL DEFAULT '' COMMENT 'ץȡ���';
alter table lianjia_house change column city city varchar(64) NOT NULL DEFAULT '' COMMENT '����';

alter table trans_history change column id id varchar(32) NOT NULL COMMENT '';
alter table trans_history change column trans_price trans_price float NOT NULL DEFAULT 0 COMMENT '�ɽ��۸�';
alter table trans_history change column trans_date trans_date date NOT NULL COMMENT '�ɽ�����';
alter table trans_history change column list_price list_price float NOT NULL DEFAULT 0 COMMENT '���Ƽ۸�';
alter table trans_history change column list_date list_date date NOT NULL DEFAULT '1970-01-01' COMMENT '��������';
alter table trans_history change column trans_age trans_age varchar(32) NOT NULL DEFAULT '' COMMENT '�ɽ�������';
alter table trans_history change column price_adjustment_times price_adjustment_times int(8) NOT NULL DEFAULT -1 COMMENT '���۴���';
alter table trans_history change column visit_times visit_times int(8) NOT NULL DEFAULT -1 COMMENT '��������';
alter table trans_history change column follow_times follow_times int(8) NOT NULL DEFAULT -1 COMMENT '��ע����';
alter table trans_history change column view_times view_times int(8) NOT NULL DEFAULT -1 COMMENT '�������';

alter table second_hand_house_sale_info change column id id varchar(32) NOT NULL COMMENT '';
alter table second_hand_house_sale_info change column list_date list_date date NOT NULL DEFAULT '1970-01-01' COMMENT '��������';
alter table second_hand_house_sale_info change column last_trans_date last_trans_date date NOT NULL DEFAULT '1970-01-01' COMMENT '�ϴν���';
alter table second_hand_house_sale_info change column trans_age trans_age varchar(32) NOT NULL DEFAULT '' COMMENT '�ɽ�������';
alter table second_hand_house_sale_info change column mortgage mortgage  varchar(32) NOT NULL DEFAULT '' COMMENT '��Ѻ��Ϣ';
alter table second_hand_house_sale_info change column certicate certicate varchar(32) NOT NULL DEFAULT '' COMMENT '��������';

alter table second_hand_house_price_info change column id id varchar(32) NOT NULL COMMENT '';
alter table second_hand_house_price_info change column list_price list_price float NOT NULL DEFAULT 0 COMMENT '���Ƽ۸�';
alter table second_hand_house_price_info change column crawl_date crawl_date date NOT NULL DEFAULT '1970-01-01' COMMENT '�۸�ץȡ����';
alter table second_hand_house_price_info change column visit_times visit_times int(8) NOT NULL DEFAULT -1 COMMENT '��������';
alter table second_hand_house_price_info change column follow_times follow_times int(8) NOT NULL DEFAULT -1 COMMENT '��ע����';