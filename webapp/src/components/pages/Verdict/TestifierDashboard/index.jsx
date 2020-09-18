import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useParams } from 'react-router-dom'
import { requestData, selectEntityByKeyAndId } from 'redux-thunk-data'

import VerdictItem from 'components/layout/VerdictItem'
import { verdictNormalizer } from 'utils/normalizers'

import Appearances from './Appearances'


export default () => {
  const dispatch = useDispatch()
  const { verdictId } = useParams()

  const verdict =  useSelector(state =>
    selectEntityByKeyAndId(state, 'verdicts', verdictId))


  useEffect(() => {
    dispatch(requestData({
      apiPath: `/verdicts/${verdictId}/appearances`,
      normalizer: verdictNormalizer
    }))
  }, [dispatch, verdictId])


  if (!verdict) return null

  return (
    <div className='testifier-dashboard'>
      <VerdictItem
        asLink={false}
        verdict={verdict}
        withLinksShares={false}
      />
      <Appearances />
    </div>
  )
}
