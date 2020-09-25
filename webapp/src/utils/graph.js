export const edgeWithDecoration = edge => edge


const colorsByNodeType = {
  'Claim': '#F00',
  'Verdict': '#900',
  'VerdictTag': '#F63',
  'Tag': '#F96',
  'User': '#CF6',
  'Role': '#CF6',
  'Medium': '#FF3',
  'Organization': '#FF3',
  'Content': '#06F',
  'Appearance': '#96F',
  'AuthorContent': '#009'
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
    label: node.id,
    size: sizesByNodeType[node.type] || 5,
    color: colorsByNodeType[node.type] || '#ccc',
  }
}
