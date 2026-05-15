from django.urls import path

from .views import (

    HomeView,
    AboutView,
    ContactView,

    PublicCourseListView,
    PublicCourseDetailView,

    EnrollView,

    PublicBlogListView,
    PublicBlogDetailView,

    PrivacyPolicyView,
    TermsOfServiceView,
    SitemapView,

    chat_api,
)

# =====================================================
# APP NAMESPACE
# =====================================================

app_name = "website"

# =====================================================
# URL PATTERNS
# =====================================================

urlpatterns = [

    # =================================================
    # HOME
    # =================================================

    path(
        "",
        HomeView.as_view(),
        name="home"
    ),

    # =================================================
    # ABOUT
    # =================================================

    path(
        "about/",
        AboutView.as_view(),
        name="about"
    ),

    # =================================================
    # CONTACT
    # =================================================

    path(
        "contact/",
        ContactView.as_view(),
        name="contact"
    ),

    # =================================================
    # COURSES
    # =================================================

    path(
        "courses/",
        PublicCourseListView.as_view(),
        name="public_course_list"
    ),

    path(
        "courses/<int:pk>/",
        PublicCourseDetailView.as_view(),
        name="public_course_detail"
    ),

    # =================================================
    # ENROLLMENT
    # =================================================

    path(
        "enroll/",
        EnrollView.as_view(),
        name="enroll"
    ),

    # =================================================
    # BLOG
    # =================================================

    path(
        "blog/",
        PublicBlogListView.as_view(),
        name="blog_list"
    ),

    path(
        "blog/<slug:slug>/",
        PublicBlogDetailView.as_view(),
        name="blog_detail"
    ),

    # =================================================
    # LEGAL PAGES
    # =================================================

    path(
        "privacy-policy/",
        PrivacyPolicyView.as_view(),
        name="privacy_policy"
    ),

    path(
        "terms-of-service/",
        TermsOfServiceView.as_view(),
        name="terms_of_service"
    ),

    path(
        "sitemap/",
        SitemapView.as_view(),
        name="sitemap"
    ),

    # =================================================
    # AI CHAT API
    # =================================================

    path(
        "chat/",
        chat_api,
        name="chat_api"
    ),

]
