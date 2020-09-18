export const edgeWithDecoration = edge => edge


const sizesByNodeType = {
  'Claim': 10,
  'Content': 3,
  'User': 1
}


export const nodeWithDecoration = node => {

  const { type } = node
  return {
    ...node,
    color: 'red',
    size: sizesByNodeType[type] || node.size,
  }
}
