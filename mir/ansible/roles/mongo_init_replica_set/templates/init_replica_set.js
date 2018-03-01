rs.initiate({
  _id: "rs0",
  members: [
    {
      _id: 0,
      host: "{{ groups['database_primary'][0] }}:27017",
      priority: 1
    }
  ]
});
