const {
  Model,
} = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Room_permission extends Model {}

  Room_permission.init({
    room_id: DataTypes.INTEGER,
    entity_UUID: DataTypes.UUID,
    level: DataTypes.INTEGER,
    permissions: DataTypes.STRING,
    kind: DataTypes.STRING,
    accepted: DataTypes.BOOLEAN,
  }, {
    sequelize,
    modelName: 'Room_permission',
  });
  Room_permission.associate = function associate(models) {
    Room_permission.belongsTo(models.Room, {
      foreignKey: 'room_id',
    });
  };
  Room_permission.removeAttribute('id');
  return Room_permission;
};
