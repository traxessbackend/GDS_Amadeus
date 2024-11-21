# Changelog 


## [0.2.0] -  2024-02-06

### Added
 1. Table `statuses` ( Values: `New`, `In_Progress`, `Completed`),  CRUD and endpoint `/api/v1/statuses/` Get All Statuses.
 2. Added fields to `topics` table:
   - Event_date  (timestamp, Optional)
   - Goal (varchar (2056), Optional)
   - status_id (smallint, FK)

  ### Changed
  1. Endpoint `/api/v1/topics/paginated`:
   - Added filters: `color_id`, `status_id`, `continent_id`, `event_date_from`, `event_date_to`
   - Added fields to response: `goal`, `reason`, `procedures`, `source`, `event_date `, `color_name`, `status_name`, `continent_name`
---
