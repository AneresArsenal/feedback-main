export const edgeWithDecoration = edge => edge


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
    color: 'red',
  }
}
