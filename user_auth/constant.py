mentor_profile_info = {
  "type": "object",
          "properties": {
            "bio": {
              "type": "string"
            },
            "skills": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "mentorship_style": {
              "type": "string"
            },
            "contact_info": {
              "type": "string",
              "format": "email"
            }
          }
}

mentee_profile_info = {
  "type": "object",
  "title": "mentee",
  "properties": {
    "bio": {
      "type": "string"
    },
    "goals": {
      "type": "array",
      "items": {
        "type": "string",
        "description": "Describe what specific areas you need guidance in (e.g., backend development, database design)."

      }
    },
    "current_skills": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "mentorship_needs": {
      "type": "string"
    },
    "contact_info": {
      "type": "string",
      "format": "email"
    }
  }
}