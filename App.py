from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

# 🔥 FB_DTSG Extractor Function
def extract_fb_dtsg(cookies):
    headers = {"Cookie": cookies}
    response = requests.get("https://www.facebook.com/", headers=headers)
    
    # ✅ Extract FB_DTSG using Regex
    fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
    if fb_dtsg_match:
        return fb_dtsg_match.group(1)
    return None

# 🔥 Token Fetcher Function
def get_facebook_token(cookies):
    fb_dtsg = extract_fb_dtsg(cookies)
    if not fb_dtsg:
        return None, "FB_DTSG extraction failed!"

    url = "https://www.facebook.com/dialog/oauth/business/cancel/"
    
    # ✅ Headers & Data
    headers = {"Cookie": cookies}
    data = {
        "fb_dtsg": fb_dtsg,
        "app_id": "124024574287414",
        "version": "v12.0",
        "logger_id": "",
        "redirect_uri": "fbconnect://success",
        "response_types[0]": "token",
        "response_types[1]": "code",
        "display": "page",
        "action": "finish",
        "return_scopes": "false",
        "return_format[0]": "access_token",
        "return_format[1]": "code",
        "set_token_expires_in_60_days": "false"
    }

    # ✅ User Scopes Add Kar Rahe Hain
    user_scopes = [
        "user_birthday", "user_religion_politics", "user_relationships",
        "user_relationship_details", "user_hometown", "user_location",
        "user_likes", "user_education_history", "user_work_history",
        "user_website", "user_events", "user_photos", "user_videos",
        "user_friends", "user_about_me", "user_posts", "email",
        "manage_fundraisers", "read_custom_friendlists", "read_insights",
        "rsvp_event", "xmpp_login", "offline_access", "publish_video",
        "openid", "catalog_management", "user_messenger_contact",
        "gaming_user_locale", "private_computation_access",
        "instagram_business_basic", "user_managed_groups",
        "groups_show_list", "pages_manage_cta", "pages_manage_instant_articles",
        "pages_show_list", "pages_messaging", "pages_messaging_phone_number",
        "pages_messaging_subscriptions", "read_page_mailboxes",
        "ads_management", "ads_read", "business_management",
        "instagram_basic", "instagram_manage_comments", "instagram_manage_insights",
        "instagram_content_publish", "publish_to_groups", "groups_access_member_info",
        "leads_retrieval", "whatsapp_business_management",
        "instagram_manage_messages", "attribution_read", "page_events",
        "business_creative_transfer", "pages_read_engagement", "pages_manage_metadata",
        "pages_read_user_content", "pages_manage_ads", "pages_manage_posts",
        "pages_manage_engagement", "whatsapp_business_messaging",
        "instagram_shopping_tag_products", "read_audience_network_insights",
        "user_about_me", "user_actions.books", "user_actions.fitness",
        "user_actions.music", "user_actions.news", "user_actions.video",
        "user_activities", "user_education_history", "user_events",
        "user_friends", "user_games_activity", "user_groups",
        "user_hometown", "user_interests", "user_likes",
        "user_location", "user_managed_groups", "user_photos",
        "user_posts", "user_relationship_details", "user_relationships",
        "user_religion_politics", "user_status", "user_tagged_places",
        "user_videos", "user_website", "user_work_history",
        "email", "manage_notifications", "manage_pages",
        "publish_actions", "publish_pages", "read_friendlists",
        "read_insights", "read_page_mailboxes", "read_stream",
        "rsvp_event", "read_mailbox", "business_creative_management",
        "business_creative_insights", "business_creative_insights_share",
        "whitelisted_offline_access"
    ]

    # ✅ Scopes Add Kar Rahe Hain
    for i, scope in enumerate(user_scopes):
        data[f"user_scopes[{i}]"] = scope

    # ✅ Send POST Request
    response = requests.post(url, headers=headers, data=data)

    # ✅ Extract Access Token
    token_match = re.search(r'access_token=([\w\d]+)', response.text)
    if token_match:
        return token_match.group(1), None
    return None, "Token extraction failed!"

# 🔥 Home Route
@app.route("/", methods=["GET", "POST"])
def home():
    token = error = None
    if request.method == "POST":
        cookies = request.form.get("cookies")
        token, error = get_facebook_token(cookies)
    return render_template("index.html", token=token, error=error)

if __name__ == "__main__":
    app.run(debug=True)
