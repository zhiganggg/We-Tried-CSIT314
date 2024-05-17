@startuml

class Profile {
    + Integer id
    + String name
    + Text description
    + DateTime date_created
    --
    + Boolean create_profile(String name, Text description)
    + Boolean update_profile(Integer profile_id, String name, Text description)
    + List<Profile> search_profile(String search_query)
    + Boolean delete_profile(Integer id)
    + List<Profile> get_all_profiles()
}

class User {
    + Integer id
    + String email
    + String first_name
    + String last_name
    + String password
    + Enum status
    + DateTime date_created
    + Integer profile_id
    --
    + User create_user(String email, String first_name, String last_name, String password, Integer profile_id)
    + Boolean update_user(Integer user_id, String email, String first_name, String last_name)
    + Boolean update_password(Integer user_id, String new_password)
    + Enum update_status(Integer id)
    + List<User> get_all_users()
    + User get_user_by_id(Integer id)
    + User get_user_by_email(String email)
    + List<User> search_user(String search_query)
}

class Agent {
    + Integer id
    + String cea_registration_no
    + String agency_license_no
    + Integer user_id
    --
    + Agent create_agent(String cea_registration_no, String agency_license_no, Integer user_id)
    + Agent get_agent_by_id(Integer id)
    + Agent get_cea_no(String cea_registration_no)
    + List<Tuple<Listing, Agent>> get_all_listings_with_agents()
}

class Listing {
    + Integer id
    + String title
    + Text description
    + String type
    + Float price
    + Integer bedrooms
    + Integer bathrooms
    + Integer size_sqft
    + String location
    + Enum availability
    + String photo
    + DateTime date_created
    + Integer user_id
    + Integer agent_id
    --
    + Boolean create_listing(String title, Text description, String type, Float price, Integer bedrooms, Integer bathrooms, Integer size_sqft, String location, String file_path, Integer user_id, Integer agent_id)
    + Listing update_listing(Integer id, String title, Text description, String type, Float price, Integer bedrooms, Integer bathrooms, Integer size_sqft, String location, String file_path)
    + Enum update_status(Integer id)
    + Boolean delete_listing(Integer id)
    + List<Listing> get_all_listings()
    + Listing get_listing_by_id(Integer id)
    + List<Listing> get_listing_by_user(Integer user_id)
    + List<Listing> get_listing_by_agent(Integer agent_id)
    + List<Listing> search_listing_by_location(String search_query)
    + List<Listing> search_listing_by_type(String type)
    + List<Listing> search_by_price_range(Float min_price, Float max_price)
    + List<Listing> search_by_min_price(Float min_price)
    + List<Listing> search_by_max_price(Float max_price)
    + List<Listing> search_by_bedrooms(Integer bedrooms)
    + List<Listing> search_by_min_bedrooms(Integer min_bedrooms)
}

class Shortlist {
    + Integer id
    + DateTime date_created
    + Integer user_id
    + Integer listing_id
    --
    + Shortlist manage_shortlist(Integer user_id, Integer listing_id)
    + Shortlist get_shortlist(Integer user_id, Integer listing_id)
    + List<Shortlist> get_shortlists_in_period(List<Integer> listing_ids, DateTime start_date, DateTime end_date)
}

class View {
    + Integer id
    + DateTime date_created
    + Integer user_id
    + Integer listing_id
    --
    + View create_view(Integer user_id, Integer listing_id)
    + List<View> get_views_in_period(List<Integer> listing_ids, DateTime start_date, DateTime end_date)
}

class Rating {
    + Integer id
    + Float rating
    + DateTime date_created
    + Integer user_id
    + Integer agent_id
    --
    + Boolean create_rating(Float rating_value, Integer user_id, Integer agent_id)
    + List<Rating> get_rating_by_agent(Integer agent_id)
    + Boolean delete_rating(Integer user_id, Integer agent_id)
}

class Review {
    + Integer id
    + Text review
    + DateTime date_created
    + Integer user_id
    + Integer agent_id
    --
    + Review create_review(Text review_value, Integer user_id, Integer agent_id)
    + List<Review> get_rating_by_agent(Integer agent_id)
    + Boolean delete_review(Integer user_id, Integer agent_id)
}

Profile "1" --> "0..*" User : has
User "1" --> "0..1" Agent : has
User "1" --> "0..*" Listing : creates
User "1" --> "0..*" Shortlist : manages
User "1" --> "0..*" View : views
User "1" --> "0..*" Rating : rates
User "1" --> "0..*" Review : reviews
Agent "1" --> "0..*" Listing : manages
Agent "1" --> "0..*" Rating : receives
Agent "1" --> "0..*" Review : receives
Listing "1" --> "0..*" Shortlist : shortlisted
Listing "1" --> "0..*" View : viewed

@enduml