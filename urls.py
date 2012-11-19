from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^laresumex/', include('laresumex.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),

    # actually our urls START FROM NOW

    #contact
    #(r'^/$',"generate_resume.views.index"),   
    (r'^common/(?P<msg>\D+)/done',"common.views.done"),
    (r'^contact',"common.views.contact"),
    
    #jobposting
    
    (r'^jobposting/add$',"jobposting.views.add"),
    (r'^jobposting/view_hidden$',"jobposting.views.hidden"),
    (r'^jobposting/(?P<template>\D+)/view$',"jobposting.views.view"),
    (r'^jobposting/(?P<template>\D+)/do$',"jobposting.views.do"),

    # generate_resume
    (r'^generate_resume/(?P<prn>\d+)/pdf',"generate_resume.views.pdf"),
    (r'^generate_resume/(?P<prn>\d+)/html',"generate_resume.views.html"),
    (r'^generate_resume/(?P<prn>\d+)/pisapdf',"generate_resume.views.pisapdf"), #the non-latex pisa and reportlab based pdf generator

    #(r'^generate_resume/(?P<prn>\d+)/latex',"generate_resume.views.latex"),
    
    #ldap_login
    (r'^ldap_login/$','ldap_login.views.login'), #for authentication
    (r'^ldap_login/logout$','ldap_login.views.logout'), #for loggin out
    (r'^home/$',"common.views.index"),
    (r'^$','common.views.index'),
    
    # company
    (r'^company/getResume',"company.views.getResume"),
    (r'^company/list',"company.views.company_list"),
    (r'^company/get_student_name',"company.views.get_students_name"),
    (r'^company/apply',"company.views.apply"),
    (r'^PT/admin',"company.views.admin_index"),
    (r'^PT/fetch',"company.views.fetch_index"),
    (r'^PT/reports',"company.views.got_placed"),
    
    
    # student_info
    (r'^student_info/(?P<prn>\d+)/edit',"student_info.views.edit"),
    (r'^student_info/form',"student_info.views.showform"),
    (r'^student_info/(?P<prn>\d+)/submit',"student_info.views.submit"),
    (r'^form',"student_info.views.showform"),

    #trying out django social auth
    #(r'^socialauth/sample/',"socialauth.views.sampleView"),
    #(r'^socialauth/login-handler/',"socialauth.views.loginHandler"),
    #(r'^socialauth/logout/',"socialauth.views.logout"), 
    #url(r'', include('social_auth.urls')),
    
)
