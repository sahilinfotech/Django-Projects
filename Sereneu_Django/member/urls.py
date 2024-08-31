from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('verify/', ActivationView.as_view()),
    path('recover/', RecoverView.as_view()),
    path('reset-otp/', ResetOtpView.as_view()),
    path('reset/', PasswordResetView.as_view()),
    path('get-profile/', ProfileInfo.as_view()),
    path('post-profile/', ProfileInformation.as_view()),
    path('pic/', ProfilePic.as_view()),
    path('calendar/', EventCalendarView.as_view()),
    path('event-list/', EventListView.as_view()),
    path('notification-list/', NotificationsView.as_view()),
    path('today-event-list/', TodayEventListView.as_view()),
    path('event-day/', EventDayView.as_view()),
    path('event-detail/', EventDetailView.as_view()),
    path('add-event/', AddEventView.as_view()),
    path('update-event/', EditEventView.as_view()),
    path('delete-event/', DeleleEventView.as_view()),
    path('mark-event/', MarkEventView.as_view()),
    path('task-count/', CompletedTasksCountView.as_view()),
    path('get-pushnotifications/', PushNotificationView.as_view()),
    path('add-pushnotifications/', AddPushNotificationView.as_view()),
    
    path('add-notes/', AddNotesFun.as_view()),
    path('update-notes/', UpdateNotesFun.as_view()),
    path('delete-notes/', DeleteNotesFun.as_view()),
    path('get-notes/', getNotesFun.as_view()),
    path('get-notesusingid/', getNotesUsingIDFun.as_view()),
    
    path('delete-user/', DeleteUserFun.as_view()),
        
    path('add-foldername/', AddfoldernameFun.as_view()),
    path('update-foldername/', UpdatefoldernameFun.as_view()),
    path('delete-foldername/', DeletefoldernameFun.as_view()),
    path('get-foldername/', getfoldernameFun.as_view()),
    path('get-foldernameid/', getfoldernameUsingIDFun.as_view()),
    
    
    
    path('add-folderfilename/', AddfolderfilenameFun.as_view()),
    path('update-folderfilename/', UpdatefolderfilenameFun.as_view()),
    path('delete-folderfilename/', DeletefolderfilenameFun.as_view()),
    # path('get-folderfilename/', getfolderfilenameFun.as_view()),
    path('get-folderfilenameid/', getfolderfilenameUsingIDFun.as_view()),
    
    
    path('add-Schedular/', AddSchedularFun.as_view()),
    path('delete-Schedular/', DeleteSchedularFun.as_view()),
    path('update-Schedular/', UpdateSchedularFun.as_view()),
    path('get-SchedularAll/', getSchedularallFun.as_view()),
    path('get-SchedularToday/', getSchedularTodayFun.as_view()),
    
    
    path('add-examdetails/', AddexamdetailsFun.as_view()),
    path('delete-examdetails/', DeleteexamdetailsFun.as_view()),
    path('update-examdetails/', UpdateexamdetailsFun.as_view()),
    path('get-examdetailsAll/', getexamdetailsallFun.as_view()),
    path('get-examdetailsToday/', getexamdetailsTodayFun.as_view()),
    
]