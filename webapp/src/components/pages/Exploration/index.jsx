import React, { useCallback, useEffect, useRef, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useParams } from 'react-router-dom'
import { requestData } from 'redux-thunk-data'

import Graph from 'components/layout/Graph'
import Header from 'components/layout/Header'
import Main from 'components/layout/Main'
import {
  componentAccessor,
  heightAccessor,
  widthAccessor
} from 'utils/exploration'

export default () => {
  const dispatch = useDispatch()
  const { collectionName, entityId } = useParams()
  const enterRef = useRef()

  const [enterElement, setEnterElement] = useState()

  const graphs = useSelector(state => state.data.graphs) || []


  const handleNodeEnter = useCallback(node => {
    if (!node) return
    console.log(node.x, node.y)
    const { clientHeight, clientWidth } = enterRef.current.parentElement.querySelector('.sigma-nodes')
    enterRef.current.style.top = `${(clientHeight / 2.) - node.y}px`
    enterRef.current.style.left = `${(clientWidth / 2.) + node.x}px`

    setEnterElement(componentAccessor(node))
  }, [enterRef, setEnterElement])


  useEffect(() => {
    let apiPath = '/graphs'
    if (collectionName && entityId) {
      apiPath = `${apiPath}/${collectionName}/${entityId}`
    }
    dispatch(requestData({ apiPath }))
  }, [collectionName, dispatch, entityId])


  return (
    <>
      <Header />
      <Main className="exploration with-header">
        <div className="container">
          <Graph
            graph={graphs[0]}
            onNodeEnter={handleNodeEnter}
          >
            <div
              className="enter"
              ref={enterRef}
            >
              {enterElement}
            </div>
          </Graph>
        </div>
      </Main>
    </>
  )
}
