import requests
import re
import json
import string
import random
import time
import os


DELAY = 1  # Delay between requests in seconds


def extract_invite_code(link):
    match = re.search(r'(?:discord\.gg/|discord\.com/invite/)([a-zA-Z0-9]+)', link)
    if match:
        return match.group(1)
    else:
        return None


def rate_limited_request(url):
    retries = 5
    retry_wait = 2  # Start with a 2-second wait

    while retries > 0:
        response = requests.get(url)

        if response.ok:
            return response
        elif response.status_code == 404:  # Invite not found
            return response
        elif response.status_code == 429:  # Rate limit exceeded
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                retry_wait = int(retry_after) + 1  # Add 1 second for safety
            else:
                retry_wait = retry_wait * 2  # Exponential backoff

            print(f"Rate limited. Retrying in {retry_wait} seconds...")
            time.sleep(retry_wait)
            retries -= 1
        else:
            print(f"Request failed with status code {response.status_code}")
            return response

    print("Maximum retries exceeded. Aborting.")
    return None


def is_invite_active(invite):
    invite_code = extract_invite_code(invite)
    if not invite_code:
        print("Invalid invite link format.")
        return False
    api_url = f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true"
    response = rate_limited_request(api_url)
    if not response:
        return False  # Rate limited or request failed

    if response.status_code == 404:
        return False  # Invite not found

    try:
        data = response.json()
        if 'message' in data and data['message'] == 'Unknown Invite':
            return False  # Invite is unknown
        else:
            return True  # Invite is active
    except ValueError:
        return False  # Error parsing JSON


def generate_random_invite():
    characters = string.ascii_letters + string.digits
    invite_code = ''.join(random.choice(characters) for _ in range(7))
    return f"https://discord.gg/{invite_code}"


def fetch_invite(invite_code):
    if not invite_code:
        return None

    url = f'https://discord.com/api/v8/invites/{invite_code}?with_counts=true'
    response = rate_limited_request(url)

    if response and response.ok:
        return response.json()
    else:
        print("Failed to fetch invite details.")
        return None


def convert_null_to_none(obj):
    for key, value in obj.items():
        if value is None:
            obj[key] = "None"
        elif isinstance(value, dict):
            convert_null_to_none(value)


def construct_avatar_url(user_id, avatar_hash):
    if user_id and avatar_hash:
        return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}?size=1024"
    else:
        return "None"


def construct_banner_url(entity_id, banner_hash):
    if entity_id and banner_hash:
        return f"https://cdn.discordapp.com/banners/{entity_id}/{banner_hash}?size=1024"
    else:
        return "None"


def construct_icon_url(guild_id, icon_hash):
    if guild_id and icon_hash:
        return f"https://cdn.discordapp.com/icons/{guild_id}/{icon_hash}?size=1024"
    else:
        return "None"


def main():
    target_active_invites = int(input("Enter the number of active invites you want to find: "))
    print(f"Searching for {target_active_invites} active Discord invites...")

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    active_invites_file = os.path.join(data_dir, "active_invites.json")
    inactive_invites_file = os.path.join(data_dir, "inactive_invites.json")
    detailed_active_invites_file = os.path.join(data_dir, "detailed_active_invites.json")

    active_invites = []
    inactive_invites = []
    detailed_active_invites = []

    id_counter = 1

    while len(active_invites) < target_active_invites:
        invite_link = generate_random_invite()
        print(f"Checking invite: {invite_link}")

        if is_invite_active(invite_link):
            invite_code = extract_invite_code(invite_link)
            invite_details = fetch_invite(invite_code)

            if invite_details:
                convert_null_to_none(invite_details)

                # Format image URLs
                inviter_id = invite_details["inviter"]["id"]
                invite_details["inviter"]["avatar"] = construct_avatar_url(inviter_id, invite_details["inviter"].get("avatar"))
                invite_details["inviter"]["banner"] = construct_banner_url(inviter_id, invite_details["inviter"].get("banner"))

                guild_id = invite_details["guild"]["id"]
                invite_details["guild"]["icon"] = construct_icon_url(guild_id, invite_details["guild"].get("icon"))
                invite_details["guild"]["banner"] = construct_banner_url(guild_id, invite_details["guild"].get("banner"))

                invite_details["id"] = id_counter
                detailed_active_invites.append(invite_details)
                with open(detailed_active_invites_file, "w") as f:
                    json.dump(detailed_active_invites, f, indent=4)

                active_invites.append(invite_link)
                with open(active_invites_file, "w") as f:
                    json.dump(active_invites, f, indent=4)

                print(f"Found an active invite: {invite_link}")
                id_counter += 1
        else:
            inactive_invites.append(invite_link)
            with open(inactive_invites_file, "w") as f:
                json.dump(inactive_invites, f, indent=4)

            print(f"Invite is inactive: {invite_link}")

        time.sleep(DELAY)

    print(f"Found {len(active_invites)} active invites.")
    print(f"Active invites have been saved to {active_invites_file}")
    print(f"Inactive invites have been saved to {inactive_invites_file}")
    print(f"Detailed active invite information has been saved to {detailed_active_invites_file}")


if __name__ == "__main__":
    main()
