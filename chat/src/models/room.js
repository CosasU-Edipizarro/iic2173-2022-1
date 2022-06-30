const {
  Model,
} = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Room extends Model {}
  Room.init({
    uuid: DataTypes.UUID,
    name: DataTypes.STRING,
    entity_owner: DataTypes.UUID,
    level_admin: DataTypes.INTEGER,
    type: DataTypes.STRING,
    max_entity_rules: DataTypes.INTEGER,
  }, {
    sequelize,
    modelName: 'Room',
  });
  Room.associate = function associate(models) {
    Room.hasMany(models.Room_permission, {
      foreignKey: 'room_id',
    });
  };
  return Room;
};
