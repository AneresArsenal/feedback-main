import PropTypes from 'prop-types'
import React, { useEffect, useMemo } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { requestData } from 'redux-thunk-data'

import selectGraphByCollectionNameAndEntityId from 'selectors/selectGraphByCollectionNameAndEntityId'
import { edgeWithDecoration, nodeWithDecoration } from 'utils/graph'

import Graph from './Graph'


const _ = ({ children, collectionName, entityId }) => {
  const dispatch = useDispatch()

  const graph = useSelector(state =>
    selectGraphByCollectionNameAndEntityId(state, collectionName, entityId))

  const graphWithDecoration = useMemo(() => graph && ({
    edges: graph.edges.map(edgeWithDecoration),
    nodes: graph.nodes.map(nodeWithDecoration)
  }), [graph])


  useEffect(() => {
    let apiPath = '/graphs'
    if (collectionName && entityId) {
      apiPath = `${apiPath}/${collectionName}/${entityId}`
    }
    dispatch(requestData({ apiPath }))
  }, [collectionName, dispatch, entityId])


  if (!graphWithDecoration) return null

  return (
    <Graph graph={graphWithDecoration}>
      {children}
    </Graph>
  )
}


_.defaultProps = {
  children: null,
  collectionName: null,
  entityId: null
}

_.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node
  ]),
  collectionName: PropTypes.string,
  entityId: PropTypes.string
}

export default _
