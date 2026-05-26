from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Role, Priority, Category, Tag,
    User, Service, Project,
    News, Article, ArticleTag,
    ContactMessage, Comment, Attachment, Notification,
)


# ─── Справочники ────────────────────────────────────────────────────────────

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'description')
    ordering     = ('level',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ─── Пользователи ───────────────────────────────────────────────────────────

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display   = ('username', 'email', 'role', 'first_name', 'last_name', 'is_active', 'created_at')
    list_filter    = ('role', 'is_active', 'is_staff')
    search_fields  = ('username', 'email', 'first_name', 'last_name')
    ordering       = ('-created_at',)
    fieldsets = (
        (None,             {'fields': ('username', 'password')}),
        ('Личные данные',  {'fields': ('first_name', 'last_name', 'email')}),
        ('Роль',           {'fields': ('role',)}),
        ('Доступ',         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Права и группы', {'classes': ('collapse',),
                            'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


# ─── Услуги ─────────────────────────────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'category', 'is_active')
    list_filter   = ('category', 'is_active')
    search_fields = ('title',)


# ─── Заявки ─────────────────────────────────────────────────────────────────

class CommentInline(admin.TabularInline):
    model  = Comment
    extra  = 0
    fields = ('user', 'text', 'created_at', 'is_edited')
    readonly_fields = ('created_at',)


class AttachmentInline(admin.TabularInline):
    model  = Attachment
    extra  = 0
    fields = ('filename', 'file_type', 'file_size')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display   = ('id', 'title', 'user', 'manager', 'service', 'priority', 'status', 'created_at')
    list_filter    = ('status', 'priority', 'service')
    search_fields  = ('title', 'user__username', 'manager__username')
    ordering       = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines        = [CommentInline, AttachmentInline]


# ─── Контент ────────────────────────────────────────────────────────────────

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'author', 'published_at')
    search_fields = ('title',)
    ordering      = ('-published_at',)


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'category', 'author', 'is_published', 'published_at')
    list_filter   = ('is_published', 'category')
    search_fields = ('title',)
    inlines       = [ArticleTagInline]


# ─── Коммуникация ───────────────────────────────────────────────────────────

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'email', 'subject', 'created_at', 'is_processed')
    list_filter   = ('is_processed',)
    search_fields = ('name', 'email', 'subject')
    ordering      = ('-created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'project', 'is_read', 'created_at')
    list_filter   = ('is_read',)
    ordering      = ('-created_at',)
