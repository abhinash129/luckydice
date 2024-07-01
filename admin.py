from django.contrib import admin

# Register your models here.
from .models import UserProfile
from .models import DepositMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'email', 'gender', 'balance']
    search_fields = ['username', 'email']


from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance',)

from .models import VirtualWallet

@admin.register(VirtualWallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance',)


from django.contrib import admin
from .models import UserAction, GameResult

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'selected_dice', 'selected_amount', 'timestamp')
    search_fields = ('user__username', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')

@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'result_images', 'bet_amount', 'won_amount', 'timestamp')
    search_fields = ('user__username', 'result_images', 'timestamp')
    list_filter = ('timestamp',) 

@admin.register(DepositMessage)
class DepositMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'date')
    search_fields = ('user__username', 'message')
    date_hierarchy = 'date'