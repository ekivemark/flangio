{
  "mapreduce" : "lymph",
  "map" : function() {
    for (var key in this) { emit(key, null); }
  },
  "reduce" : function(key, stuff) { return null; }, 
  "out": "lymph" + "_keys"
}
