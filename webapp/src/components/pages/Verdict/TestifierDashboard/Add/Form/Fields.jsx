import React, { useEffect, useMemo } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { requestData } from 'redux-thunk-data'

import HiddenField from 'components/layout/form/fields/HiddenField'
import SelectField from 'components/layout/form/fields/SelectField'
import TextField from 'components/layout/form/fields/TextField'


export default () => {
  const dispatch = useDispatch()


  const stanceTypes = useSelector(state => state.data.stanceTypes)
  const stanceOptions = useMemo(() => (stanceTypes || []).map(stanceType => ({
    label: stanceType.value.label,
    value: stanceType.key
  })), [stanceTypes])

  useEffect(() => {
    dispatch(requestData({ apiPath: '/stanceTypes' }))
  }, [dispatch])


  return (
    <div className="fields">
      <div>
        <HiddenField
          name="quotedClaimId"
          type="hidden"
        />
        <TextField
          label="URL of the article quoting this claim : "
          name="url"
          required
        />
        <SelectField
          label="What is the stance of the article for this claim :"
          name="stance"
          options={stanceOptions}
          required
        />
      </div>
    </div>
  )
}
