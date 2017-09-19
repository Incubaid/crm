
## principles

- part of CRM app

## model

source
- uid
- title
- description (markdown)
- comments 
- itenvironment (link to itenvironment obj if it exists, see assetmgmt)
- project (link to project object)
- links (list of link objects)


alert
- uid
- title
- source (link to source)
- source_id #whatever id used on source to identify where the issue comes from (recommend dot notation)
- content (markdown)
- category (dot notation, freely to be chosen by source)
- parentalert (if this is dependent on other alert)
- deviceuid (is assetmgmt used)
- componentuid (is assetmgmt used)
- starttime (auto calculated by system)
- closetime (auto calculated by system)
- state: new, confirmed, closed
- urgency: critical, urgent, normal, minor
- data (for e.g. toml, json or yaml structured content)
- escalationlevel (yellow, orrange, red, green)
- alert_profile
- comments
- tasks
- links
- owner
#can be more than 1 at same time
- type_down: bool (if there is downtime)
- type_performance: bool
- type_security: book
- type_instability: bool
- type_ui :userinterface
- type_possibledataloss

alert_profile
- uid
- name
- description (markdown)
- configuration: is toml config, depends on type of profile, what this configuration is
