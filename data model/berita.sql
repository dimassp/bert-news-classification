/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     20/05/2023 15:51:40                          */
/*==============================================================*/


drop table account;

drop table event;

drop table event_news;

drop table news;

drop table news_source;

drop table news_source_platform;

drop table notification;

drop table ref_content_type;

drop table ref_event_category;

drop table ref_region;

/*==============================================================*/
/* Table: account                                               */
/*==============================================================*/
create table account (
   username             VARCHAR(30)          not null,
   hashed_password      VARCHAR(1000)        not null,
   role_id              integer              not null,
   telegram_username    VARCHAR(25)          not null,
   constraint PK_ACCOUNT primary key (username)
);

/*==============================================================*/
/* Table: event                                                 */
/*==============================================================*/
create table event (
   event_id             SERIAL not null,
   description          VARCHAR(250)         not null,
   location             VARCHAR(100)         not null,
   constraint PK_EVENT primary key (event_id)
);

/*==============================================================*/
/* Table: event_news                                            */
/*==============================================================*/
create table event_news (
   event_id             INT4                 null,
   news_id              VARCHAR(500)         null,
   related_score        I(0)                 not null
);

/*==============================================================*/
/* Table: news                                                  */
/*==============================================================*/
create table news (
   news_id              VARCHAR(500)         not null,
   content_type_id      VARCHAR(100)         null,
   feedback_content_type_id VARCHAR(100)         null,
   event_category_id    VARCHAR(100)         null,
   feedback_event_category_id VARCHAR(100)         null,
   datetime_extracted   DATE                 not null,
   country_code         integer              not null default '62',
   region_code          integer              null default '32',
   news_source_id       VARCHAR(500)         null,
   region_level_2_code  integer              null,
   region_level_3_code  integer              null,
   region_level_4_code  integer              null,
   address              VARCHAR(125)         null,
   coordinates          VARCHAR(250)         null,
   impact_score         integer              null,
   content_text         VARCHAR(10000)       not null,
   news_source_url      VARCHAR(500)         not null,
   constraint PK_NEWS primary key (news_id)
);

/*==============================================================*/
/* Table: news_source                                           */
/*==============================================================*/
create table news_source (
   news_source_id       VARCHAR(500)         not null,
   news_source_platform_id VARCHAR(25)          null,
   description          VARCHAR(25)          not null,
   url                  VARCHAR(500)         not null,
   is_active            BOOL                 not null,
   constraint PK_NEWS_SOURCE primary key (news_source_id)
);

/*==============================================================*/
/* Table: news_source_platform                                  */
/*==============================================================*/
create table news_source_platform (
   news_source_platform_id VARCHAR(25)          not null,
   description          VARCHAR(20)          not null,
   scrapper             VARCHAR(25)          null,
   constraint PK_NEWS_SOURCE_PLATFORM primary key (news_source_platform_id)
);

/*==============================================================*/
/* Table: notification                                          */
/*==============================================================*/
create table notification (
   notification_id      SERIAL not null,
   news_id              VARCHAR(500)         null,
   username             VARCHAR(30)          null,
   is_delivered         BOOL                 not null,
   datetime_delivered   DATE                 null,
   constraint PK_NOTIFICATION primary key (notification_id)
);

/*==============================================================*/
/* Table: ref_content_type                                      */
/*==============================================================*/
create table ref_content_type (
   content_type_id      VARCHAR(25)          not null,
   description          CHAR(150)            not null,
   constraint PK_REF_CONTENT_TYPE primary key (content_type_id)
);

/*==============================================================*/
/* Table: ref_event_category                                    */
/*==============================================================*/
create table ref_event_category (
   event_category_id    VARCHAR(20)          not null,
   description          VARCHAR(100)         not null,
   icon_url             VARCHAR(125)         null,
   constraint PK_REF_EVENT_CATEGORY primary key (event_category_id)
);

/*==============================================================*/
/* Table: ref_region                                            */
/*==============================================================*/
create table ref_region (
   region_code          integer              not null,
   description          VARCHAR(25)          not null,
   centroid_coordinate  VARCHAR(20)          null,
   boundary_polygon     VARCHAR(20)          null,
   level                integer              not null,
   constraint PK_REF_REGION primary key (region_code)
);

alter table event_news
   add constraint FK_EVENT_NE_REFERENCE_EVENT foreign key (event_id)
      references event (event_id)
      on delete restrict on update restrict;

alter table event_news
   add constraint FK_EVENT_NE_REFERENCE_NEWS foreign key (news_id)
      references news (news_id)
      on delete restrict on update restrict;

alter table news
   add constraint FK_NEWS_REFERENCE_REF_EVEN foreign key (event_category_id)
      references ref_event_category (event_category_id)
      on delete restrict on update restrict;

alter table news
   add constraint FK_NEWS_REFERENCE_REF_CONT foreign key (content_type_id)
      references ref_content_type (content_type_id)
      on delete restrict on update restrict;

alter table news
   add constraint FK_NEWS_REFERENCE_NEWS_SOU foreign key (news_source_id)
      references news_source (news_source_id)
      on delete restrict on update restrict;

alter table news
   add constraint FK_NEWS_REFERENCE_REF_REGI foreign key (region_code)
      references ref_region (region_code)
      on delete restrict on update restrict;

alter table news_source
   add constraint FK_NEWS_SOU_REFERENCE_NEWS_SOU foreign key (news_source_platform_id)
      references news_source_platform (news_source_platform_id)
      on delete restrict on update restrict;

alter table notification
   add constraint FK_NOTIFICA_REFERENCE_NEWS foreign key (news_id)
      references news (news_id)
      on delete restrict on update restrict;

alter table notification
   add constraint FK_NOTIFICA_REFERENCE_ACCOUNT foreign key (username)
      references account (username)
      on delete restrict on update restrict;

