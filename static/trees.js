function toggle() {
  var elements = document.getElementsByClassName('leaf');

  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = elements[i].style.display === 'none' ? '' : 'none';
  }
}

var treetable_rowstate = [];
var treetable_callbacks = [];

function treetable_hideRow(rowId) {
  el = document.getElementById(rowId);
  el.style.display = "none";
}

function treetable_showRow(rowId) {
  el = document.getElementById(rowId);
  el.style.display = "";
}

function treetable_hasChildren(rowId) {
  res = document.getElementById(rowId + '_0');
  return (res != null);
}

function treetable_getRowChildren(rowId) {
  el = document.getElementById(rowId);
  var arr = [];
  i = 0;
  while (true) {
    childRowId = rowId + '_' + i;
    childEl = document.getElementById(childRowId);
    if (childEl) {
      arr[i] = childRowId;
    } else {
      break;
    }
    i++;
  }
  return (arr);
}

function treetable_toggleRow(rowId, state, force) {
  var rowChildren;
  var i;
  force = (force == null) ? 1 : force;
  if (state == null) {
    row_state = ((treetable_rowstate[rowId]) ? (treetable_rowstate[rowId]) : 1) * -1;
  } else {
    row_state = state;
  }
  rowChildren = treetable_getRowChildren(rowId);
  if (rowChildren.length == 0) return (false);
  for (i = 0; i < rowChildren.length; i++) {
    if (row_state == -1) {
      treetable_hideRow(rowChildren[i]);
      treetable_toggleRow(rowChildren[i], row_state, -1);
    } else {
      if (force == 1 || treetable_rowstate[rowId] != -1) {
        treetable_showRow(rowChildren[i]);
        treetable_toggleRow(rowChildren[i], row_state, -1);
      }
    }
  }
  if (force == 1) {
    treetable_rowstate[rowId] = row_state;
    treetable_fireEventRowStateChanged(rowId, row_state);
  }
  return (true);
}

function treetable_fireEventRowStateChanged(rowId, state) {
  if (treetable_callbacks['eventRowStateChanged']) {
    callback = treetable_callbacks['eventRowStateChanged'] + "('" + rowId + "', " + state + ");";
    eval(callback);
  }
}

function treetable_collapseAll() {
  table = document.getElementsByTagName("table")[1];
  rowChildren = table.getElementsByTagName('tr');
  for (i = 0; i < rowChildren.length; i++) {
    if (index = rowChildren[i].id.indexOf('_')) {
      if (index != rowChildren[i].id.lastIndexOf('_')) {
        rowChildren[i].style.display = 'none';
      }
      if (treetable_hasChildren(rowChildren[i].id)) {
        treetable_rowstate[rowChildren[i].id] = -1;
        treetable_fireEventRowStateChanged(rowChildren[i].id, -1);
      }
    }
  }
  return (true);
}

function treetable_expandAll() {
  table = document.getElementsByTagName("table")[1];
  rowChildren = table.getElementsByTagName('tr');
  for (i = 0; i < rowChildren.length; i++) {
    if (index = rowChildren[i].id.indexOf('_')) {
      rowChildren[i].style.display = '';
      if (treetable_hasChildren(rowChildren[i].id)) {
        treetable_rowstate[rowChildren[i].id] = 1;
        treetable_fireEventRowStateChanged(rowChildren[i].id, 1);
      }
    }
  }
  return (true);
}

function searchNode() {
  input = document.getElementById("searchNode");
  filter = input.value.toUpperCase();
  table = document.getElementById("tree");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.id.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.opacity = 1;
      } else {
        tr[i].style.opacity = .3;
      }
    } 
  }
}