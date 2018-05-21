use admin
db.auth("admin", "{{ mongodb_root_pass }}");
rs.add({_id: 1, host:"{{ groups['database_secondary'][0] }}:27017", priority:0.5});
