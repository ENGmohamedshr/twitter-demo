from django.contrib import admin
from .models import *
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user']  
    
   
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','post']  
    
   
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['id','user','comment']  
    
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user','content_type','object_id','content_obj']
    
      

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(CommentReply,CommentReplyAdmin)
admin.site.register(Like , LikeAdmin)
admin.site.register(Bookmarks)
