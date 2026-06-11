const databaseName = process.env.MONGO_INITDB_DATABASE || "app";
const appUser = process.env.MONGO_APP_USER || "app";
const appPassword = process.env.MONGO_APP_PASSWORD || "app-password";

const appDb = db.getSiblingDB(databaseName);

appDb.createUser({
  user: appUser,
  pwd: appPassword,
  roles: [
    {
      role: "readWrite",
      db: databaseName,
    },
  ],
});

appDb.createCollection("health_check");
appDb.health_check.insertOne({
  message: "mongodb initialized",
  createdAt: new Date(),
});
