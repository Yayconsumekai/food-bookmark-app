import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import StarRating from '../components/StarRating.vue'

describe('StarRating', () => {
  it('renders 5 star buttons', () => {
    const wrapper = mount(StarRating, {
      props: { modelValue: 0 }
    })
    const stars = wrapper.findAll('.star')
    expect(stars).toHaveLength(5)
  })

  it('fills stars up to modelValue', () => {
    const wrapper = mount(StarRating, {
      props: { modelValue: 3 }
    })
    const filled = wrapper.findAll('.star.filled')
    expect(filled).toHaveLength(3)
  })

  it('emits update:modelValue on star click', async () => {
    const wrapper = mount(StarRating, {
      props: { modelValue: 0 }
    })
    const stars = wrapper.findAll('.star')
    await stars[2].trigger('click')   // click 3rd star
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual([3])
  })

  it('does not emit when readonly', async () => {
    const wrapper = mount(StarRating, {
      props: { modelValue: 2, readonly: true }
    })
    const stars = wrapper.findAll('.star')
    await stars[4].trigger('click')
    expect(wrapper.emitted('update:modelValue')).toBeFalsy()
  })

  it('fills stars on hover when not readonly', async () => {
    const wrapper = mount(StarRating, {
      props: { modelValue: 0 }
    })
    const stars = wrapper.findAll('.star')
    await stars[1].trigger('mouseenter')   // hover 2nd star
    const filled = wrapper.findAll('.star.filled')
    expect(filled).toHaveLength(2)
  })

  it('clears hover on mouseleave', async () => {
    const wrapper = mount(StarRating, {
      props: { modelValue: 0 }
    })
    const stars = wrapper.findAll('.star')
    await stars[3].trigger('mouseenter')
    await stars[3].trigger('mouseleave')
    const filled = wrapper.findAll('.star.filled')
    expect(filled).toHaveLength(0)   // back to modelValue=0
  })
})