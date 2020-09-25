export const edgeWithDecoration = edge => edge

const labelDependingOnType = (node) => {
  
  let label;

  if (node.type == 'Claim') {
    label = node.datum.text
  } else if (node.type == 'Content') {
    label = node.datum.url
  } else if (node.type == 'Medium') {
    label = node.datum.name
  } else if (node.type == 'Organization') {
    label = node.datum.name
  } else if (node.type == 'Role') {
    label = node.datum.type
  } else if (node.type == 'Tag') {
    label = node.datum.label
  } else if (node.type == 'User') {
    label = `${node.datum.firstName} ${node.datum.lastName}`
  } else if (node.type == 'Verdict') {
    label = node.datum.title
  }  else {
    label = node.id
  }

  if (!label) {
    label = node.id
  }

  return label;
}


const colorsByNodeType = {
  'Appearance': '#96F',
  'AuthorContent': '#009',
  'Claim': '#F00',
  'Content': '#06F',
  'Medium': '#FF3',
  'Organization': '#FF3',
  'Role': '#CF6',
  'Tag': '#F96',
  'User': '#CF6',
  'Verdict': '#900',
  'VerdictTag': '#F63',
}

const sizesByNodeType = {
  'Claim': 10,
  'Content': 3,
  'User': 7
}

export const nodeWithDecoration = node => {
  return {
    ...node,
    x: Math.random(),
    y: Math.random(),
    label: labelDependingOnType(node),
    size: sizesByNodeType[node.type] || 5,
    color: colorsByNodeType[node.type] || '#ccc',
  }
}
