import React, { useCallback, useEffect } from 'react'
import { Form } from 'react-final-form'
import { useDispatch, useSelector } from 'react-redux'
import { useHistory, useLocation, useParams } from 'react-router-dom'
import {
  requestData,
  selectEntityByKeyAndId,
  selectEntitiesByKeyAndJoin
} from 'redux-thunk-data'
import { useFormidable } from 'with-react-formidable'
import { useQuery } from 'with-react-query'

import withRequiredLogin from 'components/hocs/withRequiredLogin'
import requests from 'reducers/requests'
import { verdictNormalizer } from 'utils/normalizers'

import FormFields from './FormFields'
import FormFooter from './FormFooter'


const API_PATH = '/verdicts'


export default withRequiredLogin(() => {
  const dispatch = useDispatch()
  const history = useHistory()
  const location = useLocation()
  const params = useParams()
  const { isCreatedEntity, method, readOnly } = useFormidable(location, params)
  const query = useQuery(location.search)
  const { verdictId } = params
  const { params: { sourceId } } = query
  let title
  if (isCreatedEntity) {
    title = 'Create a verdict'
  } else if (readOnly) {
    title = 'See the verdict'
  } else {
    title = "Edit the verdict"
  }

  const trending = useSelector(state =>
    selectEntitiesByKeyAndJoin(
      state,
      'trendings',
      { key: 'sourceId', value: sourceId }
  )[0])

  const verdict = useSelector(state =>
    selectEntityByKeyAndId(state, 'verdicts', verdictId))

  const { contentId } = verdict || {}

  const content = useSelector(state =>
    selectEntityByKeyAndId(state, 'contents', contentId))

  const {
    externalThumbUrl: contentExternalThumUrl,
    summary: contentSummary,
    title: contentTitle,
    url: contentUrl,
  } = { ...trending, ...content}

  const currentUserVerdictPatch = {
      contentExternalThumUrl,
      contentSummary,
      contentTitle,
      contentUrl,
      ...verdict
  }

  const { isPending } = useSelector(state =>
    state.requests['/verdicts']) || {}


  const handleSubmitVerdict = useCallback(formValues => {
    const { id } = currentUserVerdictPatch || {}
    const apiPath = `${API_PATH}/${id || ''}`
    return new Promise(resolve => {
      dispatch(requestData({
        apiPath,
        body: { ...formValues },
        handleFail: (beforeState, action) =>
          resolve(requests(beforeState.requests, action)[API_PATH].errors),
        handleSuccess: (state, action) => {
          const { payload: { datum } } = action
          const createdVerdictId = datum.id
          resolve()
          const nextUrl = `/verdicts/${createdVerdictId}`
          history.push(nextUrl)
        },
        method
      }))
    })
  }, [currentUserVerdictPatch, dispatch, history, method])


  useEffect(() => {
    dispatch(requestData({ apiPath: '/evaluations' }))
  }, [dispatch])

  useEffect(() => {
    dispatch(requestData({ apiPath: '/tags' }))
  }, [dispatch])

  useEffect(() => {
    if (isCreatedEntity) return
    dispatch(requestData({
      apiPath: `/verdicts/${verdictId}`,
      isMergingDatum: true,
      normalizer: verdictNormalizer,
    }))
  }, [dispatch, isCreatedEntity, verdictId])

  useEffect(() => {
    if (!sourceId) return
    dispatch(requestData({ apiPath: `/trendings/${sourceId}`}))
  }, [dispatch, sourceId])

  useEffect(() => {
    const { id } = currentUserVerdictPatch || {}
    if (isCreatedEntity && id) {
      history.push(`/verdicts/${id}?modification`)
    }
  })


  const renderForm = useCallback(({ handleSubmit, ...formProps }) => (
    <form
      autoComplete="off"
      className="form"
      disabled={isPending}
      noValidate
      onSubmit={handleSubmit}
    >
      <FormFields />
      <FormFooter {...formProps} />
    </form>
  ), [isPending])

  return (
    <>
      <section className="hero">
        <h1 className="title">
          {title}
        </h1>
      </section>
      <Form
        initialValues={currentUserVerdictPatch}
        onSubmit={handleSubmitVerdict}
        render={renderForm}
      />
    </>
  )
})
