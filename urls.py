from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .views import GameHistory

# from .forms import LoginForm, MyPasswordResetForm
from .views import BetListCreateView, GameResultListCreateView, WalletListCreateView

urlpatterns = [
    path('balance/', views.user_balance, name='user_balance'),
    path("", views.index, name="index"),
    path("About/", views.About, name="about"),
    path("How-to-play/", views.How_to_play, name="How-to-play"),
    path("Practice-Game/", views.PracticeGame, name="PracticeGame"),
    path("login", views.login, name="login"),
    path("signup_view", views.signup_view, name="signup_view"),
    path("logout", views.logout, name="logout"),
    path("account_activate", views.account_activate, name="account_activate"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("reset_password", views.reset_password, name="reset_password"),
    path(
        "reset_password_success",
        views.reset_password_success,
        name="reset_password_success",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("User_profile/", views.User_profile.as_view(), name="User_profile"),
    path(
        "Profile_settings/",
        views.ProfileSettingsView.as_view(),
        name="Profile_settings",
    ),
    
    path("mybalance/<str:balance>/", views.Mybalance, name="MyBalance"),
    path("mybalance/", views.Mybalance, name="MyBalanceWithoutBalance"),
    path("check_balance/", views.check_balance, name="check_balance"),
    path("success_page/<str:balance>/", views.success_page, name="success_page"),
    path("payment_view", views.payment_view, name="payment_view"),
    path("success/", views.success, name="success"),
    path("initiate_payment", views.initiate_payment, name="initiate_payment"),
    path("payment_view/<str:balance>/", views.payment_view, name="payment_view"),
    path("play_game", views.PlayGameView.as_view(), name="play_game"),
    path("Inbox/", views.Inbox, name="Inbox"),
    path("view_all_deposits/", views.view_all_deposits, name="view_all_deposits"),
    path("Withdraw/", views.Withdraw, name="Withdraw"),
    path("bank-details/", views.bank_details, name="bank_details"),
    path("upi-details/", views.upi_details_page, name="upi_details_page"),
    path("GameHistory/", views.GameHistory, name="GameHistory"),
    path("game-history/", GameHistory, name="game_history"),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("place_bet/", views.place_bet, name="place_bet"),
    path("store_game_result/", views.store_game_result, name="store_game_result"),
    path("get_won_amount/", views.get_won_amount, name="get_won_amount"),
    path("update_wallet/", views.update_wallet, name="update_wallet"),
    path("api/bets/", BetListCreateView.as_view(), name="bet-list-create"),
    path("api/wallets/", WalletListCreateView.as_view(), name="wallet-list-create"),
    path(
        "api/game-results/",
        GameResultListCreateView.as_view(),
        name="game-result-list-create",
    ),
    # Razorpay payment
    path(
        "initiate-razorpay-payment/",
        views.initiate_razorpay_payment,
        name="initiate_razorpay_payment",
    ),
    path("razorpay-callback/", views.razorpay_callback, name="razorpay_callback"),
    path("add_cash/", views.add_cash, name="add_cash"),
    path("home/", views.home, name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
